[View code on GitHub](https://github.com/creatorrr/turbo-chat/tree/master/.autodoc/docs/json/turbo_chat/bots/subqueries)

The `subqueries_bot` functionality in the `turbo-chat` project is designed to decompose a given request into a series of subqueries that can be used to query a knowledgebase. This is particularly useful in situations where a single question may require multiple pieces of information to be retrieved from the knowledgebase in order to provide a comprehensive answer.

The main function, `subqueries_bot`, takes several input parameters, including the main request, context, an example (defaulting to `default_subqueries_example`), maximum number of subqueries allowed (`max_queries`), request type, and the action to perform (e.g., "answer"). It yields a `User` object with a template and variables, generates an output using the `Generate` method, and parses the output to extract the subqueries.

For example, consider the following usage:

```python
request = "What is the least expensive cereal that is healthy and has a low calorie content but is also tasty?"
context = "User is a customer at a grocery store and is asking the question to the store manager."

subqueries = await subqueries_bot(request, context)
print(subqueries)
```

This would output a list of subqueries like:

```
[
    "What are some tasty cereal that are healthy?",
    "What are the prices of the above cereals?",
    "What is the least expensive cereal of the above?"
]
```

These subqueries can then be used to query the knowledgebase and gather the necessary information to answer the original request.

The `scratchpad.py` file defines a data structure and a template for handling parsed queries. The `ParsedQueries` class defines a structure for storing up to 10 parsed queries, with each query being an optional string. The `scratchpad` object is an instance of the `Scratchpad` class, which is parameterized with the `ParsedQueries` type and initialized with a multiline string that serves as a template for displaying the parsed queries.

The `template.py` file defines a template for generating instructions to create a plan for collecting information to answer a complex question or solve a problem. The template, `SUBQUERIES_TEMPLATE`, is a multi-line string that uses Jinja2 syntax for variable substitution and control structures. It takes several optional parameters, such as `request_type`, `solve_act`, and `max_queries`, which have default values if not provided.

Here's a sample usage of the template:

```python
from jinja2 import Template

template = Template(SUBQUERIES_TEMPLATE)
output = template.render(request_type="question", solve_act="answer", max_queries=5, context="A complex math problem", request="Solve the equation x^2 + 2x - 3 = 0")
print(output)
```

This would generate instructions for creating a plan to collect information for solving the given math problem, with a maximum of 5 queries to the knowledgebase.
