[View code on GitHub](https://github.com/creatorrr/turbo-chat/tree/master/.autodoc/docs/json/turbo_chat/types)

The `turbo-chat` project provides a framework for managing chat applications, including message handling, caching, memory management, and utility tools. The code is organized into several modules, each responsible for a specific functionality.

The `cache.py` module defines the `BaseCache` class, an abstract base class for caching agent responses. It provides a consistent interface for caching and retrieving data, allowing the project to easily switch between different cache implementations.

The `generators.py` module defines the `TurboGenWrapper` class and related types for generating messages using templates and managing chat memory. This allows developers to customize the chatbot's behavior by defining their own generator functions and configuring the generator with custom settings.

The `memory.py` module provides the `BaseMemory` class, an abstract base class for persisting conversation history and state. Concrete implementations of this class can store and manipulate conversation data in various ways, depending on the project's requirements.

The `messages.py` module handles messages in the chat system, defining the structure of messages, their roles, and providing a base class for managing collections of messages. This module is used to manage and manipulate messages in the chat system, such as rendering chat history or performing other operations on the messages.

The `misc.py` module defines the `WithSetup` class, a base class for components that require an asynchronous setup process. By using this class as a base class, the project can ensure that all components with asynchronous setup processes follow a consistent pattern, making the code easier to understand and maintain.

The `tools.py` module defines a type alias called `Tool` that represents a specific type of callable function. This type alias is used throughout the project to represent functions that perform certain operations on strings and return the result asynchronously.

Here's an example of how these components might be used together in the larger project:

```python
from turbo_chat import CustomCache, TurboGenFn, ChatClient, process_messages

# Create a custom cache instance
cache = CustomCache()

# Define a custom TurboGenTemplateFn and create a TurboGenFn instance
turbo_gen_fn = TurboGenFn(fn=custom_turbo_gen_template, settings={})

# Configure the generator with new settings
new_settings = {"setting1": "value1", "setting2": "value2"}
turbo_gen_fn = turbo_gen_fn.configure(new_settings)

# Create a ChatClient instance and set up the connection
client = ChatClient()
await client.setup(username="JohnDoe", server_address="chat.example.com")

# Process messages using a Tool function
messages = ["Hello", "How are you?"]
processed_messages = await process_messages(messages, tool=my_tool_function)
```

In this example, a custom cache instance is created, a custom generator function is defined and configured, a chat client is set up, and messages are processed using a `Tool` function. This demonstrates how the various components of the `turbo-chat` project can be used together to build a complete chat application.
