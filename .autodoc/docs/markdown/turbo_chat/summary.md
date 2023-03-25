[View code on GitHub](https://github.com/creatorrr/turbo-chat/tree/master/.autodoc/docs/json/turbo_chat)

The `turbo-chat` project provides a framework for managing chat applications, including message handling, caching, memory management, and utility tools. The code is organized into several modules, each responsible for a specific functionality.

The main entry point for the project is the `__init__.py` file, which imports and exposes various components from different submodules, such as bots, cache, chat, config, errors, memory, structs, turbo, types, and utils. This simplifies the process of using these components in other parts of the project. For example, to use the `User` class, one would simply write:

```python
from turbo_chat import User
```

The `chat.py` file provides a chat runner function, `run_chat`, which manages the conversation between a user and an AI assistant, utilizing memory and cache objects to optimize the response generation process.

The `config.py` file defines the available models for the project, which is likely a chatbot application utilizing OpenAI's GPT models. The purpose of this code is to provide a list of allowed models and a type definition for the models that can be used throughout the project.

The `errors.py` file defines custom error classes and a placeholder class for handling specific situations related to generators in the project.

The `runner.py` file is responsible for running a Turbo application using asynchronous generators. The main function in this code is `run`, which takes two arguments: `gen` and `input`. The `gen` argument is of type `TurboGenWrapper`, which is a custom type hint for the asynchronous generator. The `input` argument is optional and can be either a string or a dictionary.

The `turbo.py` file is a decorator for creating a chat application using an asynchronous generator. It provides a high-level interface for managing chat sessions, memory, caching, and debugging. The decorator can be applied to a generator function, which defines the chat application's behavior.

The project also includes several subfolders, such as `bots`, which provides various chatbot functionalities, such as question-answering, self-asking, subqueries handling, and text summarization; `cache`, which provides a simple in-memory caching mechanism; `memory`, which provides a memory management system with various storage strategies for handling chat data; `structs`, which contains code related to chat functionality, such as handling messages, processing results, and managing temporary data during chat sessions; `types`, which provides a framework for managing chat applications, including message handling, caching, memory management, and utility tools; and `utils`, which contains utility modules and functions that assist with various tasks related to language processing, retry mechanisms, template rendering, and token management in the context of a chat application.

In summary, the `turbo-chat` project offers a comprehensive framework for building and managing chat applications, with various components and utilities to handle different aspects of chat functionality, such as message handling, caching, memory management, and chatbot features.
