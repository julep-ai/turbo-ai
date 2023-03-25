[View code on GitHub](https://github.com/creatorrr/turbo-chat/blob/master/turbo_chat/utils/fn.py)

The `turbo-chat` project contains a utility function called `pick` that is used to extract specific keys from a given dictionary and return a new dictionary containing only those keys. This function can be helpful in scenarios where you need to filter out certain keys from a dictionary, for example, when processing user input or working with API responses.

The `pick` function takes three arguments:

1. `dictionary`: The input dictionary from which keys need to be extracted.
2. `keys`: A list of strings representing the keys to be picked from the input dictionary.
3. `optional`: An optional argument that, if provided, will be used as the default value for keys not found in the input dictionary. If not provided, a special class `PickOptionalOff` is used as the default value.

The function returns a new dictionary containing only the specified keys and their corresponding values from the input dictionary. If a key is not found in the input dictionary and the `optional` argument is not provided, the key will not be included in the output dictionary. If the `optional` argument is provided, the key will be included in the output dictionary with the value set to the `optional` argument.

Here's an example of how the `pick` function can be used:

```python
input_dict = {"name": "John", "age": 30, "city": "New York"}
keys_to_pick = ["name", "city"]

output_dict = pick(input_dict, keys_to_pick)
# output_dict will be {"name": "John", "city": "New York"}

keys_to_pick_with_optional = ["name", "country"]
output_dict_with_optional = pick(input_dict, keys_to_pick_with_optional, "Unknown")
# output_dict_with_optional will be {"name": "John", "country": "Unknown"}
```

In the larger project, the `pick` function can be used to filter out specific keys from dictionaries, making it easier to work with data structures and ensuring that only relevant information is processed or passed on to other parts of the application.
## Questions: 
 1. **Question:** What is the purpose of the `PickOptionalOff` class?
   **Answer:** The `PickOptionalOff` class is used as a default value for the `optional` parameter in the `pick` function. It helps to differentiate between cases when the `optional` parameter is not provided and when it is provided with a value of `None`.

2. **Question:** How does the `pick` function handle missing keys in the input dictionary?
   **Answer:** If a key is missing in the input dictionary and the `optional` parameter is not provided or is an instance of `PickOptionalOff`, the function will use the `dictionary.get(key, optional)` method, which returns the value of the key if it exists, or the value of `optional` (which is an instance of `PickOptionalOff`) if the key is missing. If the `optional` parameter is provided with a value other than an instance of `PickOptionalOff`, the function will raise a KeyError if the key is missing.

3. **Question:** What is the expected output format of the `pick` function?
   **Answer:** The `pick` function returns a new dictionary containing the specified keys from the input dictionary and their corresponding values. If a key is missing in the input dictionary and the `optional` parameter is not provided or is an instance of `PickOptionalOff`, the output dictionary will have the key with a value of an instance of `PickOptionalOff`. If the `optional` parameter is provided with a value other than an instance of `PickOptionalOff`, the output dictionary will have the key with the provided `optional` value.