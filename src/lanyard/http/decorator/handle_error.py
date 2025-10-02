from functools import wraps
from typing import (
    TYPE_CHECKING,
    Coroutine,
    Awaitable,
    Callable,
    Optional,
    Final,
    Type,
    Dict,
    Any,
)

from lanyard.http.exception import (
    HTTPResponseError,
    HTTPClientError,
    HTTPServerError,
    NotFoundError,
    UnauthorizedError,
)
from lanyard.http.response import HTTPResponse

if TYPE_CHECKING:
    from lanyard.http.base import BaseHTTP

_HTTP_ERROR_MAP: Final[Dict[int, Type[HTTPResponseError]]] = {
    401: UnauthorizedError,
    404: NotFoundError,
}


def handle_http_error(
    func: Callable[..., Awaitable[HTTPResponse]],
) -> Callable[..., Coroutine[Any, Any, HTTPResponse]]:
    """
    Decorator for handling HTTP errors in async methods.

    Works when the ``raise_for_status`` attribute is ``True``.

    :param func: An async method returning an HTTPResponse

    :raise HTTPResponseError: If an unknown HTTP error occurs
    :raise HTTPClientError: If an unknown HTTP client error occurs (4xx)
    :raise HTTPServerError: If an unknown HTTP server error occurs (5xx)
    :raise NotFoundError: If an HTTP error with code 404 occurs
    :raise UnauthorizedError: If an HTTP error with code 401 occurs

    :return: A decorated function that handles HTTP errors
    """

    @wraps(func)
    async def wrapper(self: "BaseHTTP", *args: Any, **kwargs: Any) -> HTTPResponse:
        if not getattr(self, "raise_for_status") or not self.raise_for_status:
            return await func(self, *args, **kwargs)

        response: HTTPResponse = await func(self, *args, **kwargs)

        status_code: int = response.status_code

        if 200 <= status_code <= 299:
            return response

        exception_class: Optional[Type[HTTPResponseError]] = _HTTP_ERROR_MAP.get(
            status_code
        )
        if exception_class is not None:
            raise exception_class(**response.model_dump())

        match status_code:
            case status_code if 400 <= status_code <= 499:
                raise HTTPClientError(**response.model_dump())
            case status_code if 500 <= status_code <= 599:
                raise HTTPServerError(**response.model_dump())
            case _:
                raise HTTPResponseError(**response.model_dump())

    return wrapper


__all__ = ["handle_http_error"]
