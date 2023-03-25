[View code on GitHub](https://github.com/creatorrr/turbo-chat/blob/master/turbo_chat/types/memory.py)

The `BaseMemory` class in this code serves as an abstract base class for persisting conversation history and state in the Turbo-Chat project. It inherits from `BaseMessageCollection`, `WithSetup`, and `pydantic.BaseModel` classes, which provide the necessary functionality for managing messages and setting up the memory.

The `BaseMemory` class has three abstract methods: `extend`, `get_state`, and `set_state`. These methods must be implemented by any concrete subclass of `BaseMemory`.

- `extend`: This method takes a list of `Message` objects and is responsible for adding them to the conversation history. For example, a concrete implementation might store the messages in a database or an in-memory data structure.

```python
async def extend(self, items: List[Message]) -> None:
    ...
```

- `get_state`: This method returns the current state of the conversation as a dictionary. The state might include information such as the current topic, user preferences, or other relevant data.

```python
async def get_state(self) -> dict:
    ...
```

- `set_state`: This method takes a dictionary representing the new state of the conversation and an optional `merge` flag. If `merge` is set to `True`, the new state should be merged with the existing state; otherwise, the existing state should be replaced.

```python
async def set_state(self, new_state: dict, merge: bool = False) -> None:
    ...
```

Additionally, the `BaseMemory` class provides two non-abstract methods: `append` and `prepare_prompt`.

- `append`: This method takes a single `Message` object and adds it to the conversation history by calling the `extend` method with a list containing the message.

```python
async def append(self, item: Message) -> None:
    await self.extend([item])
```

- `prepare_prompt`: This method takes an optional `max_tokens` parameter and returns a list of `MessageDict` objects representing the conversation history. This list can be used as a prompt for an AI model, such as OpenAI's GPT-3. The method can be overridden in subclasses to add filtering or other transformations to the message history.

```python
async def prepare_prompt(
    self,
    max_tokens: int = 0,
) -> List[MessageDict]:
    messages: List[MessageDict] = await self.get_dicts()
    return messages
```

In summary, the `BaseMemory` class provides a foundation for managing conversation history and state in the Turbo-Chat project. Concrete implementations of this class can store and manipulate conversation data in various ways, depending on the specific requirements of the project.
## Questions: 
 1. **Question**: What is the purpose of the `BaseMemory` class and how does it relate to the overall functionality of the `turbo-chat` project?
   **Answer**: The `BaseMemory` class serves as an abstract base class for persisting conversation history and state in the `turbo-chat` project. It provides a common interface for different memory implementations to store and manage chat messages and state.

2. **Question**: How are the `extend`, `get_state`, and `set_state` methods expected to be implemented in subclasses of `BaseMemory`?
   **Answer**: The `extend`, `get_state`, and `set_state` methods are marked as abstract methods, meaning that any subclass of `BaseMemory` must provide their own implementation for these methods to handle the storage and retrieval of chat messages and state.

3. **Question**: What is the purpose of the `prepare_prompt` method and how does it interact with the message history?
   **Answer**: The `prepare_prompt` method is responsible for turning the message history into a prompt for OpenAI. By default, it retrieves the message history as a list of dictionaries using the `get_dicts()` method, but it can be overridden in subclasses to add filtering or other transformations to the message history before it is used as a prompt.