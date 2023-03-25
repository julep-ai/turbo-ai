FAQ
===

Auto-generated using [autodoc](https://github.com/context-labs/autodoc#get-started).

*****

### Tell me about turbo-chat in a nutshell.

Turbo-chat is a framework for managing chat applications, including message handling, caching, memory management, and utility tools. The project is organized into several modules, each responsible for specific functionality. The main entry point is the `__init__.py` file, which imports and exposes various components from different submodules, such as bots, cache, chat, config, errors, memory, structs, turbo, types, and utils ([View code on GitHub](https://github.com/creatorrr/turbo-chat/tree/master/.autodoc/docs/json/turbo_chat)).

Turbo-chat provides various chatbot functionalities, such as question-answering, self-asking, subqueries handling, and text summarization, organized in separate modules for easy import and use ([View code on GitHub](https://github.com/creatorrr/turbo-chat/tree/master/.autodoc/docs/json/turbo_chat/bots)).

The project also includes a framework for managing chat applications, with components like BaseCache, TurboGenWrapper, BaseMemory, and message handling ([View code on GitHub](https://github.com/creatorrr/turbo-chat/tree/master/.autodoc/docs/json/turbo_chat/types)).

Turbo-chat offers a memory management system with various storage strategies for handling chat data, such as LocalMemory, LocalTruncatedMemory, and LocalSummarizeMemory ([View code on GitHub](https://github.com/creatorrr/turbo-chat/tree/master/.autodoc/docs/json/turbo_chat/memory)).

In summary, turbo-chat is a comprehensive framework for building and managing chat applications, with various components and utilities to handle different aspects of chat functionality.


Turbo-chat is a framework for managing chat applications, including message handling, caching, memory management, and utility tools. The project is organized into several modules, each responsible for specific functionality. The main entry point is the __init__.py file, which imports and exposes various components from different submodules, such as bots, cache, chat, config, errors, memory, structs, turbo, types, and utils (View code on GitHub (https://github.com/creatorrr/turbo-chat/tree/master/.autodoc/docs/json/turbo_chat)).

Turbo-chat provides various chatbot functionalities, such as question-answering, self-asking, subqueries handling, and text summarization, organized in separate modules for easy import and use (View code on GitHub (https://github.com/creatorrr/turbo-chat/tree/master/.autodoc/docs/json/turbo_chat/bots)).

The project also includes a framework for managing chat applications, with components like BaseCache, TurboGenWrapper, BaseMemory, and message handling (View code on GitHub (https://github.com/creatorrr/turbo-chat/tree/master/.autodoc/docs/json/turbo_chat/types)).

Turbo-chat offers a memory management system with various storage strategies for handling chat data, such as LocalMemory, LocalTruncatedMemory, and LocalSummarizeMemory (View code on GitHub (https://github.com/creatorrr/turbo-chat/tree/master/.autodoc/docs/json/turbo_chat/memory)).

In summary, turbo-chat is a comprehensive framework for building and managing chat applications, with various components and utilities to handle different aspects of chat functionality.


*****

### Tell me more about async generators and how they are used in this library

The `turbo` decorator in the turbo-chat library is a parameterized decorator for creating a chat application from an async generator. It provides a high-level interface for managing chat sessions, memory, caching, and debugging. The decorator can be applied to a generator function, which defines the chat application's behavior. It takes various settings as input, such as memory_class, model, stream, cache_class, and debug, and wraps the given async generator function with additional functionality, such as initializing memory and cache, handling different types of outputs, and managing the generator's lifecycle.

The `turbo` decorator handles different types of outputs by checking the type of the output and performing specific actions accordingly. For example, if the output is a Result, it yields the output; if it's a Message, it appends it to memory and yields it if the forward flag is set; if it's a BaseMessageCollection, it extends the memory; if it's a GetInput, it appends an Assistant message to memory and waits for user input; and if it's a Generate, it runs the chat and yields the generated result if needed.

The `turbo` decorator handles debugging and logging through the optional `debug` parameter, which is a callable function. If the `debug` function is provided, the decorator logs the inputs and outputs of the wrapped generator by calling the `debug` function with a dictionary containing the app name, timestamp, type (input or output), and payload (input or output data).

Here's an example of how to use the `turbo` decorator:

```python
from turbo_chat import turbo, GetInput, Generate

@turbo()
async def my_chat_app():
    user_input = yield GetInput("What's your name?")
    yield Generate(f"Hello, {user_input}. How can I help you today?", forward=True)
```

In this example, the `turbo` decorator is applied to the `my_chat_app` generator function. The generator yields a `GetInput` object to request the user's name and then yields a `Generate` object to create a response using the OpenAI API. The `forward=True` flag indicates that the generated response should be forwarded to the user.

[View code on GitHub](https://github.com/creatorrr/turbo-chat/blob/master/turbo_chat/turbo.py)


The turbo decorator in the turbo-chat library is a parameterized decorator for creating a chat application from an async generator. It provides a high-level interface for managing chat sessions, memory, caching, and debugging. The decorator can be applied to a generator function, which defines the chat application's behavior. It takes various settings as input, such as memory_class, model, stream, cache_class, and debug, and wraps the given async generator function with additional functionality, such as initializing memory and cache, handling different types of outputs, and managing the generator's lifecycle.

The turbo decorator handles different types of outputs by checking the type of the output and performing specific actions accordingly. For example, if the output is a Result, it yields the output; if it's a Message, it appends it to memory and yields it if the forward flag is set; if it's a BaseMessageCollection, it extends the memory; if it's a GetInput, it appends an Assistant message to memory and waits for user input; and if it's a Generate, it runs the chat and yields the generated result if needed.

The turbo decorator handles debugging and logging through the optional debug parameter, which is a callable function. If the debug function is provided, the decorator logs the inputs and outputs of the wrapped generator by calling the debug function with a dictionary containing the app name, timestamp, type (input or output), and payload (input or output data).

Here's an example of how to use the turbo decorator:

```python
    from turbo_chat import turbo, GetInput, Generate

    @turbo()
    async def my_chat_app():
        user_input = yield GetInput("What's your name?")
        yield Generate(f"Hello, {user_input}. How can I help you today?", forward=True)

```

In this example, the turbo decorator is applied to the my_chat_app generator function. The generator yields a GetInput object to request the user's name and then yields a Generate object to create a response using the OpenAI API. The forward=True flag indicates that the generated response should be forwarded to the user.

View code on GitHub (https://github.com/creatorrr/turbo-chat/blob/master/turbo_chat/turbo.py)


*****

### Give me an example of how to use turbo-chat to write a simple ping bot

To create a simple ping bot using turbo-chat, you can define a custom generator function and use the `turbo` decorator. Here's an example:

```python
from turbo_chat import turbo, User, Generate

@turbo
async def ping_bot(user_input: str):
    if user_input.lower() == "ping":
        user = User("pong")
        yield user
        yield Generate()

async def main():
    async for response in ping_bot("ping"):
        print(response)

await main()
```

In this example, the `ping_bot` function checks if the user input is "ping" (case-insensitive). If it is, the function creates a `User` object with the message "pong" and yields it. Then, it yields a `Generate` object, which might be used by the larger project to trigger the generation of the response. The `main` function demonstrates how to use the `ping_bot` function in an asynchronous context.

Please note that this example assumes you have access to the `turbo`, `User`, and `Generate` components from the turbo-chat project. You can find more information about these components in the [turbo-chat GitHub repository](https://github.com/creatorrr/turbo-chat/tree/master/.autodoc/docs/json/turbo_chat).


To create a simple ping bot using turbo-chat, you can define a custom generator function and use the turbo decorator. Here's an example:

```python
    from turbo_chat import turbo, User, Generate

    @turbo
    async def ping_bot(user_input: str):
        if user_input.lower() == "ping":
            user = User("pong")
            yield user
            yield Generate()

    async def main():
        async for response in ping_bot("ping"):
            print(response)

    await main()
    
```

In this example, the ping_bot function checks if the user input is "ping" (case-insensitive). If it is, the function creates a User object with the message "pong" and yields it. Then, it yields a Generate object, which might be used by the larger project to trigger the generation of the response. The main function demonstrates how to use the ping_bot function in an asynchronous context.

Please note that this example assumes you have access to the turbo, User, and Generate components from the turbo-chat project. You can find more information about these components in the turbo-chat GitHub repository (https://github.com/creatorrr/turbo-chat/tree/master/.autodoc/docs/json/turbo_chat).


*****

### Write a simple chat app using turbo-chat that acts as a therapist and talks to the user in a loop.

Sure! Here's an example of a simple chat app using `turbo-chat` that acts as a therapist and continuously interacts with the user in a loop. First, you'll need to create an asynchronous generator function that defines the chat application's behavior. In this case, the generator function will act as a therapist and respond to the user's input.

```python
import asyncio
from turbo_chat import turbo, run_chat

@turbo
async def therapist_chat(user_input):
    # You can customize the therapist's behavior here.
    # For simplicity, we'll just echo the user's input.
    response = f"I understand that you're saying: {user_input}"
    return response

async def main():
    print("Welcome to the therapist chat!")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        response = await run_chat(therapist_chat, user_input)
        print(f"Therapist: {response}")

asyncio.run(main())
```

In this example, the `therapist_chat` function is decorated with the `@turbo` decorator, which provides a high-level interface for managing chat sessions, memory, caching, and debugging. The `main` function runs an infinite loop that takes user input and calls the `run_chat` function with the `therapist_chat` generator and the user's input. The chat will continue until the user types "exit".

Please note that this is a very basic example, and you can customize the therapist's behavior by modifying the `therapist_chat` function. You might want to use the [qa_bot](https://github.com/creatorrr/turbo-chat/tree/master/.autodoc/docs/json/turbo_chat/bots) or other functionalities provided by the `turbo-chat` project to make the therapist more interactive and intelligent.

Here are some reference links to GitHub:

- [turbo_chat](https://github.com/creatorrr/turbo-chat/tree/master/.autodoc/docs/json/turbo_chat)
- [turbo_chat/bots](https://github.com/creatorrr/turbo-chat/tree/master/.autodoc/docs/json/turbo_chat/bots)
- [turbo_chat/types](https://github.com/creatorrr/turbo-chat/tree/master/.autodoc/docs/json/turbo_chat/types)
- [turbo_chat/memory](https://github.com/creatorrr/turbo-chat/tree/master/.autodoc/docs/json/turbo_chat/memory)


Sure! Here's an example of a simple chat app using turbo-chat that acts as a therapist and continuously interacts with the user in a loop. First, you'll need to create an asynchronous generator function that defines the chat application's behavior. In this case, the generator function will act as a therapist and respond to the user's input.

```python
    import asyncio
    from turbo_chat import turbo

    @turbo
    async def therapist_chat(user_input):
        # You can customize the therapist's behavior here.
        # For simplicity, we'll just echo the user's input.
        response = f"I understand that you're saying: {user_input}"
        return response

    async def main():
        print("Welcome to the therapist chat!")
        while True:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                break
            response = await therapist_chat.run(user_input)
            print(f"Therapist: {response.content}")

    asyncio.run(main())

```

In this example, the therapist_chat function is decorated with the @turbo decorator, which provides a high-level interface for managing chat sessions, memory, caching, and debugging. The main function runs an infinite loop that takes user input and calls the run_chat function with the therapist_chat generator and the user's input. The chat will continue until the user types "exit".

Please note that this is a very basic example, and you can customize the therapist's behavior by modifying the therapist_chat function. You might want to use the qa_bot (https://github.com/creatorrr/turbo-chat/tree/master/.autodoc/docs/json/turbo_chat/bots) or other functionalities provided by the turbo-chat project to make the therapist more interactive and intelligent.

Here are some reference links to GitHub:

    * turbo_chat (https://github.com/creatorrr/turbo-chat/tree/master/.autodoc/docs/json/turbo_chat)
    * turbo_chat/bots (https://github.com/creatorrr/turbo-chat/tree/master/.autodoc/docs/json/turbo_chat/bots)
    * turbo_chat/types (https://github.com/creatorrr/turbo-chat/tree/master/.autodoc/docs/json/turbo_chat/types)
    * turbo_chat/memory (https://github.com/creatorrr/turbo-chat/tree/master/.autodoc/docs/json/turbo_chat/memory)


*****

### write an example of using redis as a cache for turbo-chat apps

In the `turbo-chat` project, the provided caching mechanism is the `SimpleCache` class, which is an in-memory cache. However, you can create a custom cache implementation using Redis by extending the `BaseCache` class. Here's an example of how to create a custom Redis cache for the turbo-chat application:

```python
import aioredis
from turbo_chat.cache import BaseCache

class RedisCache(BaseCache):
    async def setup(self):
        self.redis = await aioredis.create_redis_pool("redis://localhost")

    async def has(self, key: str) -> bool:
        return await self.redis.exists(key)

    async def set(self, key: str, value: str) -> None:
        await self.redis.set(key, value)

    async def get(self, key: str) -> str:
        return await self.redis.get(key, encoding="utf-8")

    async def clear(self) -> None:
        await self.redis.flushdb()
```

To use this custom Redis cache in your turbo-chat application, simply create an instance of the `RedisCache` class and use it as you would with the `SimpleCache` class:

```python
from turbo_chat import RedisCache

cache = RedisCache()
await cache.setup()

# Store a key-value pair in the cache
await cache.set("key1", "value1")

# Check if a key exists in the cache
print(await cache.has("key1"))  # Output: True

# Retrieve the value associated with a key from the cache
print(await cache.get("key1"))  # Output: "value1"

# Clear the cache
await cache.clear()
print(await cache.has("key1"))  # Output: False
```

This example demonstrates how to create a custom Redis cache for the turbo-chat project by extending the `BaseCache` class and implementing the required methods. You can find more information about the `BaseCache` class in the [turbo-chat/cache package](https://github.com/creatorrr/turbo-chat/tree/master/.autodoc/docs/json/turbo_chat/cache).


In the turbo-chat project, the provided caching mechanism is the SimpleCache class, which is an in-memory cache. However, you can create a custom cache implementation using Redis by extending the BaseCache class. Here's an example of how to create a custom Redis cache for the turbo-chat application:

```python
    import aioredis
    from turbo_chat.cache import BaseCache

    class RedisCache(BaseCache):
        async def setup(self):
            self.redis = await aioredis.create_redis_pool("redis://localhost")

        async def has(self, key: str) -> bool:
            return await self.redis.exists(key)

        async def set(self, key: str, value: str) -> None:
            await self.redis.set(key, value)

        async def get(self, key: str) -> str:
            return await self.redis.get(key, encoding="utf-8")

        async def clear(self) -> None:
            await self.redis.flushdb()

```

To use this custom Redis cache in your turbo-chat application, simply create an instance of the RedisCache class and use it as you would with the SimpleCache class:

```python
    from turbo_chat import RedisCache

    cache = RedisCache()
    await cache.setup()

    # Store a key-value pair in the cache
    await cache.set("key1", "value1")

    # Check if a key exists in the cache
    print(await cache.has("key1"))  # Output: True

    # Retrieve the value associated with a key from the cache
    print(await cache.get("key1"))  # Output: "value1"

    # Clear the cache
    await cache.clear()
    print(await cache.has("key1"))  # Output: False

```

This example demonstrates how to create a custom Redis cache for the turbo-chat project by extending the BaseCache class and implementing the required methods. You can find more information about the BaseCache class in the turbo-chat/cache package (https://github.com/creatorrr/turbo-chat/tree/master/.autodoc/docs/json/turbo_chat/cache).


*****

### write an example of using sqlite for saving memory and state from the `BaseMemory` class

In the turbo-chat project, there isn't a direct example of using SQLite for saving memory and state by extending the `BaseMemory` class. However, I can guide you through creating a custom implementation using SQLite.

First, you'll need to create a new class that extends the `BaseMemory` class. You can call it `SQLiteMemory`. In this class, you'll need to implement the `extend`, `get_state`, and `set_state` methods, as well as any additional methods required for interacting with SQLite.

Here's a basic outline of the `SQLiteMemory` class:

```python
import sqlite3
from typing import List
from turbo_chat.types.memory import BaseMemory, Message

class SQLiteMemory(BaseMemory):
    def __init__(self, db_path: str):
        super().__init__()
        self.db_path = db_path
        self._initialize_database()

    def _initialize_database(self):
        # Create the SQLite database and tables if they don't exist

    async def extend(self, items: List[Message]) -> None:
        # Add the messages to the SQLite database

    async def get_state(self) -> dict:
        # Retrieve the state from the SQLite database

    async def set_state(self, new_state: dict, merge: bool = False) -> None:
        # Update the state in the SQLite database
```

You'll need to implement the `_initialize_database` method to create the SQLite database and tables if they don't exist. Then, implement the `extend`, `get_state`, and `set_state` methods to interact with the SQLite database for storing and retrieving messages and state.

Once you have implemented the `SQLiteMemory` class, you can use it in your application like this:

```python
sqlite_memory = SQLiteMemory(db_path="my_database.db")
await sqlite_memory.extend([Message(...)])
chat_history = await sqlite_memory.get()
```

This is just a starting point, and you'll need to fill in the details for interacting with the SQLite database. You can refer to the [SQLite documentation](https://docs.python.org/3/library/sqlite3.html) for more information on how to work with SQLite in Python.

Reference links:
- [BaseMemory class](https://github.com/creatorrr/turbo-chat/blob/master/turbo_chat/types/memory.py)
- [LocalMemory class](https://github.com/creatorrr/turbo-chat/blob/master/turbo_chat/memory/local_memory.py)


In the turbo-chat project, there isn't a direct example of using SQLite for saving memory and state by extending the BaseMemory class. However, I can guide you through creating a custom implementation using SQLite.

First, you'll need to create a new class that extends the BaseMemory class. You can call it SQLiteMemory. In this class, you'll need to implement the extend, get_state, and set_state methods, as well as any additional methods required for interacting with SQLite.

Here's a basic outline of the SQLiteMemory class:

```python
    import sqlite3
    from typing import List
    from turbo_chat.types.memory import BaseMemory, Message

    class SQLiteMemory(BaseMemory):
        def __init__(self, db_path: str):
            super().__init__()
            self.db_path = db_path
            self._initialize_database()

        def _initialize_database(self):
            # Create the SQLite database and tables if they don't exist

        async def extend(self, items: List[Message]) -> None:
            # Add the messages to the SQLite database

        async def get_state(self) -> dict:
            # Retrieve the state from the SQLite database

        async def set_state(self, new_state: dict, merge: bool = False) -> None:
            # Update the state in the SQLite database
```

You'll need to implement the _initialize_database method to create the SQLite database and tables if they don't exist. Then, implement the extend, get_state, and set_state methods to interact with the SQLite database for storing and retrieving messages and state.

Once you have implemented the SQLiteMemory class, you can use it in your application like this:

```python
    sqlite_memory = SQLiteMemory(db_path="my_database.db")
    await sqlite_memory.extend([Message(...)])
    chat_history = await sqlite_memory.get()
```

This is just a starting point, and you'll need to fill in the details for interacting with the SQLite database. You can refer to the SQLite documentation (https://docs.python.org/3/library/sqlite3.html) for more information on how to work with SQLite in Python.

Reference links:

    * BaseMemory class (https://github.com/creatorrr/turbo-chat/blob/master/turbo_chat/types/memory.py)
    * LocalMemory class (https://github.com/creatorrr/turbo-chat/blob/master/turbo_chat/memory/local_memory.py)

