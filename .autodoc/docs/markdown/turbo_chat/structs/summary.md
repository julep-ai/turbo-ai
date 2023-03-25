[View code on GitHub](https://github.com/creatorrr/turbo-chat/tree/master/.autodoc/docs/json/turbo_chat/structs)

The `turbo-chat/structs` folder contains code related to chat functionality, such as handling messages, processing results, and managing temporary data during chat sessions. It provides a single point of import for these components, simplifying their usage in other parts of the project.

`messages.py` defines various message types and an example message collection. These classes can be used to create and manage different types of messages in the chat application, such as system messages, user messages, and assistant messages. The `Example` class can be used to create example message collections for testing or demonstration purposes.

`proxies.py` defines a `TurboGenWrapper` class and a `proxy_turbo_gen_fn` function, which create a proxy wrapper around generator functions, allowing them to be used asynchronously and providing a consistent interface for running them. For example:

```python
@proxy_turbo_gen_fn
def my_generator(input):
    # Generator logic here
    yield result

async def main():
    # Create an instance of the wrapped generator
    wrapped_gen = my_generator("some input")

    # Use the wrapped generator as an async iterator
    async for result in wrapped_gen:
        # Process the result asynchronously
        pass

    # Run the wrapped generator with a specific input
    result = await wrapped_gen.run("another input")
```

`result.py` defines a `Result` class that holds the result yielded by a turbo app. It stores the content of a message, whether the message requires user input, and whether the message processing is done. For example:

```python
# Create a message object with content
message = SomeMessage(content="Hello, world!")

# Create a Result instance from the message object
result = Result.from_message(message, done=True)

# Check if the result needs input and if it's done
if result.needs_input:
    # Get user input and process it
    pass
elif result.done:
    # Handle the completed result
    pass
```

`scratchpad.py` contains a `Scratchpad` class that parses input strings according to a given specification, extracting structured data from unstructured text input. For example:

```python
spec = "Name: {name}\nAge: {age:d}\nActive: {active:bool}"
input_str = "Name: John\nAge: 25\nActive: yes"

scratchpad = Scratchpad(spec)
result = scratchpad.parse(input_str)

print(result)  # Output: {'name': 'John', 'age': 25, 'active': True}
```

`signals.py` handles signals related to user input and completion generation using Pydantic models as placeholders for specific actions. The `Generate` class is used to indicate that the completion generation process should be run, while the `GetInput` class is used to indicate that user input is required.

In summary, the `turbo-chat/structs` folder provides various components related to chat functionality, making it easier for other parts of the project to access and use these components.
