class HTTPXError(Exception):
    def __init__(
        self,
        message: str,
    ) -> None:
        """
        A base exception for all errors related to the HTTPX library-based client.

        :param message: Error message.
        """

        self.message: str = message

        super().__init__(self.message)


class ContextRequiredError(HTTPXError):
    def __init__(self) -> None:
        """
        Exception when it is necessary to use context.
        """

        super().__init__("Use an asynchronous context")


__all__ = [
    "HTTPXError",
    "ContextRequiredError",
]
