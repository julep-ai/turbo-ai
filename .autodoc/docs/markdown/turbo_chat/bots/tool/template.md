[View code on GitHub](https://github.com/creatorrr/turbo-chat/blob/master/turbo_chat/bots/tool/template.py)

This code defines a template for a chatbot conversation in the Turbo-Chat project. The chatbot acts as a facilitator between the user and an expert, relaying messages between them and providing the expert with a set of tools to assist the user.

The `TOOLBOT_TEMPLATE` is a Jinja2 template that generates a formatted conversation script. It includes optional prologue and additional information sections, instructions for the expert, and a list of available tools. The template also specifies the format for user messages, expert responses, and tool usage.

The conversation starts with the chatbot introducing the user type and providing instructions to the expert. The expert's responses should be in the format `Response: <what you want to say>`. The chatbot will relay these responses to the user.

The expert has access to a set of tools, which are listed in the template. To use a tool, the expert must reply in the following format:

```
{{user_type | capitalize}} said: <what the {{user_type}} said>
Thought: Need to use a tool? <Yes or No>
Tool: <the name of the tool to use>
Tool Input: <the input to the tool in the format specified by the tool>
```

The chatbot will then provide the result of the tool in the format `Tool Result: <the result of the tool you used>`.

The `EXAMPLE_TEMPLATE` is another Jinja2 template that wraps an example conversation between the expert and the user. It is used to provide examples of how the conversation should be conducted.

In the larger project, these templates can be used to generate conversation scripts for various user types and scenarios, helping the expert to assist users effectively using the available tools.
## Questions: 
 1. **Question:** What is the purpose of the `TOOLBOT_TEMPLATE` and `EXAMPLE_TEMPLATE` variables in this code?
   **Answer:** The `TOOLBOT_TEMPLATE` and `EXAMPLE_TEMPLATE` variables store string templates for generating a formatted conversation between the user and the toolbot. They are used to structure the conversation and provide instructions on how to interact with the toolbot and use the available tools.

2. **Question:** How are the tools and their documentation added to the `Tools` section in the `TOOLBOT_TEMPLATE`?
   **Answer:** The tools are added to the `Tools` section using a for loop `{% for tool in tools %}` that iterates through the `tools` list. For each tool, the tool's name (`{{tool.__name__}}`) and documentation (`{{tool.__doc__}}`) are added to the template.

3. **Question:** How does the code handle the case when there is additional information to be provided in the `TOOLBOT_TEMPLATE`?
   **Answer:** The code checks if the `additional_info` variable is present using `{% if additional_info -%}`. If it is present, the additional information is added to the template using `{{additional_info}}`.