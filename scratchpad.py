#############
## Imports ##
#############

from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from functools import wraps
import multiprocessing
import os
from types import TracebackType
from typing import AsyncIterator, Generator, Generic, Hashable, List, Optional, Type, TypedDict, TypeVar

from docarray import BaseDoc, DocList
from docarray.index.abstract import BaseDocIndex
from docarray.index.backends.weaviate import EmbeddedOptions, WeaviateDocumentIndex
from docarray.typing import NdArray
from pydantic import Field


#####################
## Async Generator ##
#####################

TSend = TypeVar('TSend', contravariant=True)
TYield = TypeVar('TYield', covariant=True)

class AsyncGenerator(ABC, AsyncIterator[TYield], Generic[TYield, TSend]):
    @abstractmethod
    def __aiter__(self) -> AsyncIterator[TYield]:
        return self
    
    @abstractmethod
    async def __anext__(self) -> TYield:  # throws: StopAsyncIteration, ...
        return await self.asend(None)

    @abstractmethod
    async def asend(
        self,
        input: Optional[TSend]
    ) -> TYield:  # throws: StopAsyncIteration, ...
        ...

    @abstractmethod
    async def athrow(
        self,
        exc_type: Type[BaseException],
        exc_value: Optional[BaseException] = None,
        traceback: Optional[TracebackType] = None,
    ) -> Optional[TYield]:  # throws: exc_type, StopAsyncIteration, ...
        ...
    
    @abstractmethod
    async def aclose(
        self
    ) -> None:  # throws RuntimeError, ...
        try:
            await self.athrow(GeneratorExit)
        except (GeneratorExit, StopAsyncIteration):
            pass
        else:
            raise RuntimeError("...")
            

#############
## Structs ##
#############

class ChatMLRole(str, Enum):
    System = "system"
    User = "user"
    Assistant = "assistant"

class ChatMLDict(TypedDict):
    role: ChatMLRole
    content: str

class ChatMLMessage(BaseDoc):
    role: ChatMLRole
    content: str

class MessageMetadata(BaseDoc):
    timestamp: datetime = Field(default_factory=datetime.now)
    tags: list[str] = []
    extra: dict[str, Hashable] = {}

class Message(ChatMLMessage):
    metadata: MessageMetadata = Field(default_factory=MessageMetadata)

class User(Message):
    role: ChatMLRole = ChatMLRole.User

class Assistant(Message):
    role: ChatMLRole = ChatMLRole.Assistant

class System(Message):
    role: ChatMLRole = ChatMLRole.System


TSignal = TypeVar('TSignal')
class Signal(Generic[TSignal], MessageMetadata):
    content: TSignal
    needs_input: bool = False
    done: bool = False

class Start(Signal[TSignal]):
    pass

class GetInput(Signal[TSignal]):
    needs_input: bool = True

class Result(Signal[TSignal]):
    done: bool = True

class EmbeddingMessage(Message):
    embedding: NdArray[OPENAI_EMBEDDING_DIMS] = Field(
        dims=OPENAI_EMBEDDING_DIMS,
        is_embedding=True,
    )

###############
## Constants ##
###############

OPENAI_EMBEDDING_DIMS: int = 1536
CPU_COUNT: int = multiprocessing.cpu_count()
TURBO_DATA_DIR: str = os.environ.get("TURBO_DATA_DIR", "./.turbo_chat")


#####################
## Weaviate Config ##
#####################

def get_weaviate_index(**dbconfig_params):
    if not dbconfig_params:
        dbconfig_params = dict(
            embedded_options=EmbeddedOptions(
            persistence_data_path=f"{TURBO_DATA_DIR}/weaviate-embedded"
        )

    dbconfig = WeaviateDocumentIndex.DBConfig(**dbconfig_params)
    
    return WeaviateDocumentIndex[Message](db_config=dbconfig)
    
def get_weaviate_runtime_config(**options):

    batch_config = dict(
        batch_size=20,
        dynamic=True,
        timeout_retries=3,
        num_workers=CPU_COUNT // 2,
    )
    
    batch_config = {**batch_config, **options}
    runtime_config = WeaviateDocumentIndex.RuntimeConfig(batch_config=batch_config)
    
    return runtime_config
    
############
## Memory ##
############

class BaseMemory(DocList[Message]):
    index: Optional[BaseDocIndex[Message]] = None

    def sorted(self) -> "BaseMemory":
        return sorted(
            self,
            key=lambda doc: doc.metadata.timestamp,
            reverse=True,
        )

    async def process(self, **kwargs) -> None:
        ...

    @abstractmethod
    def to_prompt(self, **kwargs) -> List[ChatMLDict]:
        raise NotImplementedError


class Memory(BaseMemory):
    def to_prompt(self, **kwargs) -> List[ChatMLDict]:
        return [
            ChatMLDict(role=message.role, content=message.content)
            for message in self.sorted()
        ]


class WeaviateMemory(BaseMemory):
    index: WeaviateDocumentIndex[Message] = Field(
        default_factory=lambda: WeaviateDocumentIndex[Message](db_config=dbconfig)
    )

    def __init__(self, **data):
        super().__init__(**data)
        self.index.configure(runtime_config)

    def to_prompt(self, **kwargs) -> List[ChatMLDict]:
        raise NotImplementedError

#####################
## Turbo Generator ##
#####################

class AsyncTurboGenerator(AsyncGenerator):
    def __init__(self, func, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.func = func
        self._gen = func(*args, **kwargs)

    def __aiter__(self) -> AsyncIterator[TYield]:
        return self._gen
    
    async def __anext__(self) -> TYield:  # throws: StopAsyncIteration, ...
        return await self.asend(None)

    async def asend(
        self,
        input: Optional[TSend] = None,
    ) -> TYield:  # throws: StopAsyncIteration, ...
        return await self._gen.asend(input)

    async def athrow(
        self,
        exc_type: Type[BaseException],
        exc_value: Optional[BaseException] = None,
        traceback: Optional[TracebackType] = None,
    ) -> Optional[TYield]:  # throws: exc_type, StopAsyncIteration, ...
        print(exc_type, exc_value, traceback)
    
    async def aclose(
        self
    ) -> None:  # throws RuntimeError, ...
        try:
            await self.athrow(GeneratorExit)
        except (GeneratorExit, StopAsyncIteration):
            pass
        else:
            raise RuntimeError("...")


class TurboGenerator(Generator):
    pass


###################
## Turbo Factory ##
###################

# Type them using paramspec, generic and protocol
TurboFactory = Type[TurboGenerator]
AsyncTurboFactory = Type[AsyncTurboGenerator]

#####################
## turbo decorator ##
#####################

# turbo: (gen_fn) -> TurboFactory
# turbo: (async_gen_fn) -> AsyncTurboFactory
# turbo: (**opts) -> (gen|asyncgen) -> TurboFactory|AsyncTurboFactory

def turbo(
    fn: Optional[] = None,
    /,
    memory_class: Type[BaseMemory] = LocalTruncatedMemory,
    cache_class: Optional[Type[BaseCache]] = None,
):
    @wraps(func)
    def wrapper(*args, **kwargs):
        turbo_gen = TurboGenerator(func, *self.args, **self.kwargs)
        return turbo_gen

    return wrapper

###################
## Instantiation ##
###################

@turbo()
async def app_factory():
    for i in range(10):
        print(i)
        yield i

app = app_factory()

await app.init()
# Equivalent to:
### await app.asend(None)

result = await app.run()  # Throws if GetInput is used
reply = await app.message(input())


##################
## Sync version ##
##################

@turbo(
    experimental={
        "enable_persistence": True,  # Enables app.dumps()
        "enable_beartype": True,  # Enables beartype runtime-checking
    },
)
def sync_app_factory():
    for i in range(10):
        print(i)
        yield i

# This returns a synchronous generator instead
sync_app = sync_app_factory()

# If persistence is enabled, you can pickle the generator
pickled = sync_app.dumps()

# And reload using
sync_app = sync_app_factory.loads(pickled)

# Otherwise, as usual but synchronous
sync_app.init()
# Equivalent to:
### app.send(None)

result = sync_app.run()
reply = sync_app.message(input())
