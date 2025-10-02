from functools import wraps
from typing import (
    Coroutine,
    Awaitable,
    Callable,
    TypeVar,
    Any,
)

from lanyard.http.exception import UnauthorizedError
from lanyard.exception import NoPermissionError

R = TypeVar("R")


def handle_error(
    func: Callable[..., Awaitable[R]],
) -> Callable[..., Coroutine[Any, Any, R]]:
    """
    A decorator that handles certain HTTP errors and converts them into API Wrapper exceptions.

    :param func: Async method to be decorated

    :raise NoPermissionError: When the request returns ``Unauthorized status (401)``

    :return: Decorated function with error handling
    """

    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> R:
        try:
            return await func(*args, **kwargs)
        except UnauthorizedError:
            raise NoPermissionError()

    return wrapper


__all__ = ["handle_error"]
