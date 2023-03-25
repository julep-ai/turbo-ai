[View code on GitHub](https://github.com/creatorrr/turbo-chat/tree/master/.autodoc/docs/json/turbo_chat/bots/tool)

The `tool_bot` folder contains code for a chatbot that handles user queries and provides responses using a set of tools. It is designed to work with the OpenAI GPT-3.5-turbo model.

`__init__.py` serves as an entry point for importing the `tool_bot` functionality, making it easy for other modules to access and use the `tool_bot` class and its associated methods. The `__all__` variable ensures that only the necessary names are imported when using wildcard imports.

`bot.py` contains the `tool_bot` function, an asynchronous chatbot that listens for user input and processes it using a set of tools. It takes a list of tools, an optional prologue, user type, instruction, example, and a maximum number of iterations as input parameters. Here's an example of how the `tool_bot` function might be used:

```python
tools = [GetInformation, Calculate, Translate]
prologue = "Welcome to Turbo Chat!"
user_type = "customer"
instruction = "Ask me anything, and I'll try to help you using my available tools."

await tool_bot(tools, prologue, user_type, instruction)
```

`scratchpad.py` defines a data structure and a template for handling tools in the project. The `ParsedTools` class is a `TypedDict` that manages the parsed information related to tools, such as their names, inputs, and responses. The `scratchpad` variable is an instance of the `Scratchpad` class, which handles templates related to the `ParsedTools` data structure. Here's an example of how this code might be used:

```python
parsed_tools = ParsedTools(
    should_use_tool=True,
    tool_name="Example Tool",
    tool_input="Sample Input",
    final_response="Sample Output"
)

formatted_output = scratchpad.format(parsed_tools)
print(formatted_output)
```

`template.py` defines a Jinja2 template for a chatbot conversation, where the chatbot acts as a facilitator between the user and an expert. The `TOOLBOT_TEMPLATE` generates a formatted conversation script, including optional prologue and additional information sections, instructions for the expert, and a list of available tools. The `EXAMPLE_TEMPLATE` wraps an example conversation between the expert and the user.

In the larger project, these components can be used to create a chatbot that assists users effectively using the available tools, manage and format the information related to tools, and generate conversation scripts for various user types and scenarios.
