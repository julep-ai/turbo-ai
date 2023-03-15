from abc import ABC, abstractmethod
from functools import wraps
import inspect
import json
import os
from typing import (
    Any,
    AsyncGenerator,
    Callable,
    Dict,
    List,
    Literal,
    Optional,
    Protocol,
    Tuple,
    Type,
    Union,
)

import openai
import pydantic

from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)


__all__ = [
    "System",
    "User",
    "Assistant",
    "ExampleUser",
    "ExampleAssistant",
    "Generate",
    "GetUserInput",
    "InvalidValueYieldedError",
    "GeneratorAlreadyExhaustedError",
    "TurboGen",
    "MessageRole",
    "PrefixMessage",
    "BasePrefixMessageCollection",
    "BaseMemory",
    "Example",
    "BaseCache",
    "SimpleCache",
    "turbo",
    "run",
]


# Set up openai credentials
openai.organization = os.getenv("OPENAI_ORGANIZATION", None)
openai.api_key = os.environ["OPENAI_API_KEY"]


# Enums
# Allowed values for openai chatml prefixes
MessageRole = Literal[
    "system",
    "user",
    "assistant",
    "system name=example_user",
    "system name=example_assistant",
]

# Allowed chatgpt model names
TurboModel = Literal[
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-0301",
]


# Models
class PrefixMessage(pydantic.BaseModel):
    """Container for a single chatml prefix message"""

    role: MessageRole
    content: str
    yield_downstream: bool = False


class System(PrefixMessage):
    """System message"""

    role: MessageRole = "system"


class User(PrefixMessage):
    """User message"""

    role: MessageRole = "user"


class Assistant(PrefixMessage):
    """Assistant message"""

    role: MessageRole = "assistant"
    yield_downstream: bool = True


class ExampleUser(PrefixMessage):
    """User example message"""

    role: MessageRole = "system name=example_user"


class ExampleAssistant(PrefixMessage):
    """Assistant example message"""

    role: MessageRole = "system name=example_assistant"


# Utility classes
class Generate(pydantic.BaseModel, extra=pydantic.Extra.allow):
    """Placeholder value to indicate that completion should be run"""

    yield_downstream: bool = True


class GetUserInput(pydantic.BaseModel):
    """Placeholder value to indicate that user input is needed"""

    message: str = "User input needed"


class GeneratorAlreadyExhausted(pydantic.BaseModel):
    """Placeholder value to indicate that the generator was already exhausted"""

    ...


class InvalidValueYieldedError(ValueError):
    """Invalid value yielded by generator"""

    ...


class GeneratorAlreadyExhaustedError(StopAsyncIteration):
    """Generator was already exhausted"""

    ...


# Abstract classes
class BasePrefixMessageCollection(ABC):
    """Base class for async collections of prefix messages"""

    @abstractmethod
    async def get(self) -> List[PrefixMessage]:
        ...

    async def get_dicts(self) -> List[Dict[str, str]]:
        messages = await self.get()
        return [message.dict(include={"role", "content"}) for message in messages]


class BaseCache(ABC):
    """Base class for caching agent responses"""

    def serialize(self, obj: Any) -> Any:
        return obj

    def deserialize(self, hashed: Any) -> Any:
        return hashed

    def to_key(self, obj: Any) -> str:
        return json.dumps(self.serialize(obj))

    @abstractmethod
    async def has(self, key: Any) -> bool:
        ...

    @abstractmethod
    async def set(self, key: Any, value: Any) -> None:
        ...

    @abstractmethod
    async def get(self, key: Any) -> Any:
        ...

    @abstractmethod
    async def clear(self) -> Any:
        ...


class BaseMemory(BasePrefixMessageCollection):
    """Base class for interface for persisting prefix messages for a session"""

    async def init(self, context={}) -> None:
        ...

    @abstractmethod
    async def append(self, item: PrefixMessage) -> None:
        ...

    @abstractmethod
    async def clear(self) -> None:
        ...

    async def extend(self, items: List[PrefixMessage]) -> None:
        for item in items:
            await self.append(item)


# Types
TurboGen = AsyncGenerator[Union[Assistant, GetUserInput], Any]
TurboGenTemplate = AsyncGenerator[PrefixMessage, Any]


class TurboGenTemplateFn(Protocol):
    def __call__(
        self,
        memory: Optional[BaseMemory] = None,
        **context,
    ) -> TurboGenTemplate:
        ...


class TurboGenFn(Protocol):
    fn: TurboGenTemplateFn

    def __call__(
        self,
        **context,
    ) -> TurboGen:
        ...


# Abstract implementations
class Example(BasePrefixMessageCollection, pydantic.BaseModel):
    user: str
    assistant: str

    async def get(self) -> List[PrefixMessage]:
        return [
            ExampleUser(content=self.user),
            ExampleAssistant(content=self.assistant),
        ]


class ListMemory(BaseMemory, pydantic.BaseModel):
    """Store messages in an in-memory list"""

    messages: List[PrefixMessage] = []

    async def get(self) -> List[PrefixMessage]:
        return [
            message for message in self.messages if isinstance(message, PrefixMessage)
        ]

    async def append(self, item) -> None:
        self.messages.append(item)

    async def clear(self) -> None:
        self.messages = []


class SimpleCache(BaseCache, pydantic.BaseModel):
    """Simple in-memory cache"""

    cache: dict = {}

    async def has(self, key) -> bool:
        return self.to_key(key) in self.cache

    async def set(self, key, value) -> None:
        self.cache[self.to_key(key)] = self.serialize(value)

    async def get(self, key) -> Any:
        assert await self.has(key), "No cache entry found"
        return self.deserialize(self.cache[self.to_key(key)])

    async def clear(self) -> Any:
        self.cache = {}


# Retries
def create_retry_decorator(
    min_seconds: int = 4,
    max_seconds: int = 10,
    max_retries: int = 5,
) -> Callable[[Any], Any]:
    # Wait 2^x * 1 second between each retry starting with
    # 4 seconds, then up to 10 seconds, then 10 seconds afterwards
    return retry(
        reraise=True,
        stop=stop_after_attempt(max_retries),
        wait=wait_exponential(multiplier=1, min=min_seconds, max=max_seconds),
        retry=(
            retry_if_exception_type(openai.error.Timeout)
            | retry_if_exception_type(openai.error.APIError)
            | retry_if_exception_type(openai.error.APIConnectionError)
            | retry_if_exception_type(openai.error.RateLimitError)
            | retry_if_exception_type(openai.error.ServiceUnavailableError)
        ),
    )


# Decorator
def turbo(
    memory_class: Type[BaseMemory] = ListMemory,
    model: TurboModel = "gpt-3.5-turbo",
    stream: bool = False,
    cache: Optional[BaseCache] = None,
    log: Optional[Callable[[Any], None]] = None,
    **kwargs,
) -> Callable[[TurboGenTemplateFn], TurboGenFn]:
    """Parameterized decorator for creating a chatml app from an async generator"""

    # Streaming not supported yet
    if stream:
        raise NotImplementedError("Streaming not supported yet")

    # Prepare openai args
    chat_completion_args = {
        **kwargs,
        "model": model,
        "stream": stream,
    }

    # Create tenacity retry decorator
    with_retries = create_retry_decorator()

    # Chat runner
    @with_retries
    async def run_chat(memory: BaseMemory, **kwargs) -> Assistant:
        """Run ChatCompletion for the memory so far"""

        # Get messages from memory
        messages = await memory.get_dicts()
        if cache and await cache.has(messages):
            cached = await cache.get(messages)
            return Assistant(**cached)

        # Create completion
        args = {
            **chat_completion_args,
            **kwargs,
        }

        chat_completion = await openai.ChatCompletion.acreate(
            messages=messages,
            **args,
        )

        # Parse result
        output = chat_completion.choices[0].message
        payload = dict(content=output["content"])
        result = Assistant(**payload)

        # Append result to memory
        await memory.append(result)

        # Add to cache
        if cache:
            await cache.set(messages, payload)

        return result

    # Parameterized decorator fn
    def wrap_turbo_gen_fn(gen_fn: TurboGenTemplateFn) -> TurboGenFn:
        """Wrapper for chatml app async generator"""

        @wraps(gen_fn)
        async def turbo_gen_fn(**context) -> TurboGen:
            """Wrapped chatml app from an async generator"""

            # Init memory
            memory = memory_class()
            await memory.init(context)

            # Init generator
            signature = inspect.signature(gen_fn)
            arg_names = [k for k in signature.parameters.keys()]

            if "memory" in arg_names:
                context["memory"] = memory

            turbo_gen = gen_fn(**context)

            # Parameters
            payload: Any = None

            try:
                while True:
                    # Step through the wrapped generator
                    output = await turbo_gen.asend(payload)
                    payload = None

                    if log:
                        log(output)

                    # Add to memory
                    if isinstance(output, PrefixMessage):
                        await memory.append(output)

                        # Yield to user if yield_downstream
                        if output.yield_downstream:
                            yield output

                    elif isinstance(output, BasePrefixMessageCollection):
                        await memory.extend(output)

                    # Yield to user if GetUserInput
                    elif isinstance(output, GetUserInput):
                        payload = yield output
                        assert payload, f"User input was required, {payload} passed"

                    # Generate result
                    elif isinstance(output, Generate):
                        output_dict = output.dict()
                        yield_downstream = output_dict.pop("yield_downstream")

                        payload = await run_chat(memory, **output_dict)

                        # Yield generated result if needed
                        if yield_downstream:
                            yield payload

                    else:
                        raise InvalidValueYieldedError(
                            f"Invalid value yielded by generator: {type(output)}"
                        )

            except StopAsyncIteration:
                # Generator over, exit
                pass

        # Add reference to the original function
        turbo_gen_fn.fn = gen_fn

        return turbo_gen_fn

    return wrap_turbo_gen_fn


async def run(
    gen: TurboGen,
    input: Optional[str] = None,
) -> Tuple[Union[Assistant, GetUserInput], bool]:
    """Run a turbo app"""

    # Set placeholder values
    done = False
    output = GeneratorAlreadyExhausted()

    # Run generator
    try:
        while not isinstance(output := await gen.asend(input), GetUserInput):
            pass

    # Generator exhausted, mark done
    except StopAsyncIteration:
        done = True

    # Output is still placeholder? Raise error
    if isinstance(output, GeneratorAlreadyExhausted):
        raise GeneratorAlreadyExhaustedError()

    return (output, done)
