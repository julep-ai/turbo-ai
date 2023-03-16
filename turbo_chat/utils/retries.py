from typing import (
    Any,
    Callable,
)

import openai

from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)


__all__ = [
    "create_retry_decorator",
    "with_retries",
]


# Retries
def create_retry_decorator(
    min_seconds: int = 4,
    max_seconds: int = 10,
    max_retries: int = 5,
) -> Callable[[Any], Any]:
    # Wait 2^x * 1 second between each retry starting with
    # 4 seconds, then up to 10 seconds, then 10 seconds afterwards
    return retry(
        reraise=True,
        stop=stop_after_attempt(max_retries),
        wait=wait_exponential(multiplier=1, min=min_seconds, max=max_seconds),
        retry=(
            retry_if_exception_type(openai.error.Timeout)
            | retry_if_exception_type(openai.error.APIError)
            | retry_if_exception_type(openai.error.APIConnectionError)
            | retry_if_exception_type(openai.error.RateLimitError)
            | retry_if_exception_type(openai.error.ServiceUnavailableError)
        ),
    )


# Default retry decorator
with_retries = create_retry_decorator()
