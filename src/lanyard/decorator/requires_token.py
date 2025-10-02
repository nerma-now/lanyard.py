from functools import wraps
from typing import (
    TYPE_CHECKING,
    Coroutine,
    Awaitable,
    Callable,
    TypeVar,
    Any,
)

from lanyard.exception import TokenRequiredError

if TYPE_CHECKING:
    from lanyard.service import BaseService

R = TypeVar("R")


def requires_token(
    func: Callable[..., Awaitable[R]],
) -> Callable[..., Coroutine[Any, Any, R]]:
    """
    A decorator that ensures that a token is present before making an httpx request.

    Throws an exception when the ``token`` attribute is missing or is ``False``.

    :param func: Async method

    :raise TokenRequiredError: Token is missing

    :return: Decorated function that checks for the presence of a token
    """

    @wraps(func)
    async def wrapper(self: "BaseService", *args: Any, **kwargs: Any) -> R:
        if not getattr(self, "_context") or self._context.config.token is None:
            raise TokenRequiredError()

        return await func(self, *args, **kwargs)

    return wrapper


__all__ = ["requires_token"]
