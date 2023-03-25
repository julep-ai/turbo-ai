[View code on GitHub](https://github.com/creatorrr/turbo-chat/tree/master/.autodoc/docs/json/turbo_chat/memory)

The `turbo-chat` project provides a memory management system with various storage strategies for handling chat data. The memory management system is located in the `.autodoc/docs/json/turbo_chat/memory` folder and consists of several classes that offer different storage and processing capabilities.

The `LocalMemory` class provides a basic in-memory storage solution for messages and state data. It can be used for testing or small-scale applications where persistence is not required. Example usage:

```python
local_memory = LocalMemory()
chat_history = await local_memory.get()
```

The `LocalTruncatedMemory` class extends `LocalMemory` and implements a truncated memory storage. It ensures that the total number of tokens in the chat history does not exceed the model's context window. This can be useful for managing memory usage in situations where only recent chat data is relevant. Example usage:

```python
memory = LocalTruncatedMemory(model=TurboModel)
truncated_prompt = await memory.prepare_prompt(max_tokens=100)
```

The `LocalSummarizeMemory` class also extends `LocalMemory` and focuses on providing a summarized view of the chat data. It can be used to generate a condensed version of the chat history, which can be useful for providing an overview of the conversation or for generating reports. Example usage:

```python
summarized_memory = LocalSummarizeMemory()
summarized_chat_data = await summarized_memory.prepare_prompt()
```

By providing different memory storage implementations, the code allows the turbo-chat project to easily switch between different storage strategies depending on the requirements of the application.
