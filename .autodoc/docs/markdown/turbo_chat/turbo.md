[View code on GitHub](https://github.com/creatorrr/turbo-chat/blob/master/turbo_chat/turbo.py)

The `turbo` code is a decorator for creating a chat application using an asynchronous generator. It provides a high-level interface for managing chat sessions, memory, caching, and debugging. The decorator can be applied to a generator function, which defines the chat application's behavior.

The `turbo` decorator takes several optional parameters:

- `memory_class`: A custom memory class (default is `LocalMemory`).
- `model`: The OpenAI model to use (default is `"gpt-3.5-turbo"`).
- `stream`: Whether to use streaming (not supported yet).
- `cache_class`: A custom cache class.
- `debug`: A callable for debugging purposes.
- `**kwargs`: Additional keyword arguments for the OpenAI API.

The decorator wraps the generator function with a `turbo_gen_fn` function, which initializes the memory and cache classes, sets up the generator, and handles the different types of outputs yielded by the generator. The wrapped generator function can yield various types of objects, such as `Result`, `Message`, `BaseMessageCollection`, `GetInput`, and `Generate`. The `turbo_gen_fn` processes these objects accordingly, updating the memory, forwarding messages, and generating responses using the OpenAI API.

The `turbo_gen_fn` also supports debugging by passing a callable to the `debug` parameter. The debug function will receive input and output payloads with additional metadata, such as the generator function name and timestamp.

Here's an example of how to use the `turbo` decorator:

```python
from turbo_chat import turbo, GetInput, Generate

@turbo()
async def my_chat_app():
    user_input = yield GetInput("What's your name?")
    yield Generate(f"Hello, {user_input}. How can I help you today?", forward=True)
```

In this example, the `turbo` decorator is applied to the `my_chat_app` generator function. The generator yields a `GetInput` object to request the user's name and then yields a `Generate` object to create a response using the OpenAI API. The `forward=True` flag indicates that the generated response should be forwarded to the user.
## Questions: 
 1. **Question**: What is the purpose of the `turbo` decorator and how does it work?
   **Answer**: The `turbo` decorator is a parameterized decorator for creating a chatml app from an async generator. It takes various settings as input, such as memory_class, model, stream, cache_class, and debug. It wraps the given async generator function (gen_fn) with additional functionality, such as initializing memory and cache, handling different types of outputs, and managing the generator's lifecycle.

2. **Question**: How does the `turbo` decorator handle different types of outputs from the wrapped generator?
   **Answer**: The `turbo` decorator handles different types of outputs by checking the type of the output and performing specific actions accordingly. For example, if the output is a Result, it yields the output; if it's a Message, it appends it to memory and yields it if the forward flag is set; if it's a BaseMessageCollection, it extends the memory; if it's a GetInput, it appends an Assistant message to memory and waits for user input; and if it's a Generate, it runs the chat and yields the generated result if needed.

3. **Question**: How does the `turbo` decorator handle debugging and logging?
   **Answer**: The `turbo` decorator handles debugging and logging through the optional `debug` parameter, which is a callable function. If the `debug` function is provided, the decorator logs the inputs and outputs of the wrapped generator by calling the `debug` function with a dictionary containing the app name, timestamp, type (input or output), and payload (input or output data).