[View code on GitHub](https://github.com/creatorrr/turbo-chat/tree/master/.autodoc/docs/json/turbo_chat/utils)

The `turbo_chat/utils` folder contains utility modules and functions that assist with various tasks related to language processing, retry mechanisms, template rendering, and token management in the context of a chat application.

For example, the `lang.py` module provides an `inflect` function that inflects words based on their grammatical tags. This can be useful when generating or manipulating text, such as generating responses in a chatbot or analyzing user input:

```python
inflected_word = inflect("run", "VBD")
print(inflected_word)  # Output: "ran"
```

The `retries.py` module defines a retry mechanism for handling API calls. It provides a `create_retry_decorator` function and a `with_retries` decorator that can be applied to any function or method that makes API calls, ensuring that temporary issues like timeouts or rate limits are handled gracefully:

```python
@with_retries
def make_api_call():
    # Code to make an API call
    pass
```

The `template.py` module is responsible for rendering templates using the Jinja2 templating engine. It provides a `render_template` function that renders templates with optional validation of the input variables:

```python
template_string = "Hello, {{ name|inflect('capitalize') }}!"
variables = {"name": "john"}
rendered_string = render_template(template_string, variables, check=True)
print(rendered_string)  # Output: "Hello, John!"
```

The `tokens.py` module provides utility functions to work with OpenAI models, focusing on token counting and handling model-specific token limits. It implements two functions: `get_max_tokens_length` and `count_tokens`:

```python
messages = [{"content": "Hello, how are you?"}, {"content": "I'm fine, thank you!"}]
model = TurboModel("gpt-3.5-turbo")
total_tokens = count_tokens(messages, model)
```

The `args.py` module provides utility functions to work with function arguments, ensuring that the required arguments for a specific function are provided when calling that function:

```python
def example_function(a, b, c=3, *, d, e=5):
    pass

args = {'a': 1, 'b': 2, 'd': 4}
result = ensure_args(example_function, args)
# result will be True
```

The `fn.py` module contains a utility function called `pick` that extracts specific keys from a given dictionary and returns a new dictionary containing only those keys:

```python
input_dict = {"name": "John", "age": 30, "city": "New York"}
keys_to_pick = ["name", "city"]

output_dict = pick(input_dict, keys_to_pick)
# output_dict will be {"name": "John", "city": "New York"}
```

These utility modules and functions can be used throughout the `turbo-chat` project to simplify various tasks and improve the overall code quality and maintainability.
