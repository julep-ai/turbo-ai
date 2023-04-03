# flake8: noqa
# This is so ruff doesn't remove * imports

import inspect
from jinja2 import Environment
from jinja2schema import infer, to_json_schema
from jsonschema import validate

from .args import get_fn_signature
from .lang import inflect

__all__ = [
    "render_template",
]

# jinja environment
jinja_env: Environment = Environment(
    autoescape=False,
    trim_blocks=True,
    lstrip_blocks=True,
)

# Add custom filters
jinja_env.filters["inflect"] = inflect
jinja_env.filters["fn_signature"] = get_fn_signature
jinja_env.filters["fn_doc"] = inspect.getdoc


# Funcs
def render_template(template_string: str, variables: dict, check: bool = False) -> str:
    # Parse template
    template = jinja_env.from_string(template_string)

    # If check is required, get required vars from template and validate variables
    if check:
        schema = to_json_schema(infer(template_string))
        validate(instance=variables, schema=schema)

    # Render
    rendered = template.render(**variables)
    return rendered
