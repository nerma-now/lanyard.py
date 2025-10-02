from typing import Any


class HTTPError(Exception):
    def __init__(
        self,
        method: str,
        url: str,
        message: str,
    ) -> None:
        """
        Base exception for all HTTP-related errors.

        :param method: Method of the request.
        :param url: URL of the request.
        :param message: Error message.
        """

        self.method: str = method
        self.url: str = url
        self.message: str = message

        super().__init__(f"{self.method} {self.url} returned: {self.message}")


class HTTPResponseError(Exception):
    def __init__(
        self,
        method: str,
        url: str,
        status_code: int,
        content: Any,
    ) -> None:
        """
        Base exception for all HTTP-related response errors.

        :param method: Method of HTTP response.
        :param url: URL of HTTP response.
        :param status_code: HTTP status code of HTTP response.
        :param content: Content of HTTP response.
        """

        self.method: str = method
        self.url: str = url
        self.status_code: int = status_code
        self.content: Any = content

        super().__init__(
            f"{self.method} {self.url} returned {self.status_code}: {self.content}"
        )


class HTTPClientError(HTTPResponseError):
    """
    Exception for HTTP related client errors (4xx).
    """

    ...


class HTTPServerError(HTTPResponseError):
    """
    Exception for HTTP related server errors (5xx).
    """

    ...


class UnauthorizedError(HTTPClientError):
    """
    Exception for HTTP client error related to "unauthorized" (401) error.
    """

    ...


class NotFoundError(HTTPClientError):
    """
    Exception for HTTP client error related to "not found" (404) error.
    """

    ...


__all__ = [
    "HTTPError",
    "HTTPResponseError",
    "HTTPClientError",
    "HTTPServerError",
    "UnauthorizedError",
    "NotFoundError",
]
