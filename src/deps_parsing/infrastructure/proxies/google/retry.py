from functools import wraps
from typing import Any, Callable

__all__ = ["retry_with_callback"]


def retry_with_callback(
    function: Callable[..., Any],
    callback: Callable[..., None],
    retries: int = 1,
) -> Callable[..., Any]:
    @wraps(function)
    def wrapper(*args, **kwargs):
        for attempt in range(retries + 1):
            try:
                return function(*args, **kwargs)
            except Exception:
                if attempt < retries:
                    callback()
                else:
                    raise

    return wrapper
