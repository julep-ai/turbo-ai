from datetime import datetime
from functools import wraps
import inspect
from typing import (
    Any,
    Callable,
    Optional,
    Type,
)


from .chat import run_chat
from .errors import InvalidValueYieldedError
from .memory import ListMemory

from .types import (
    BaseCache,
    BaseMemory,
    BasePrefixMessageCollection,
    Generate,
    GetUserInput,
    PrefixMessage,
    TurboGen,
    TurboModel,
)

from .types.generators import (
    TurboGenFn,
    TurboGenTemplateFn,
)


__all__ = [
    "turbo",
]


# Decorator
def turbo(
    memory_class: Type[BaseMemory] = ListMemory,
    model: TurboModel = "gpt-3.5-turbo",
    stream: bool = False,
    cache: Optional[BaseCache] = None,
    log: Optional[Callable[[dict], None]] = None,
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

                    # Pass inputs & outputs to debug log if needed
                    if log:
                        params = dict(
                            app=gen_fn.__name__,
                            timestamp=datetime.utcnow(),
                        )

                        payload and log({**params, "type": "input", "payload": payload})
                        output and log({**params, "type": "output", "output": output})

                    payload = None

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

                        payload = await run_chat(
                            memory,
                            cache,
                            **{
                                **chat_completion_args,
                                **output_dict,
                            },
                        )

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
