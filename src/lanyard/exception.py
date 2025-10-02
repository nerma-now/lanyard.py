class LanyardError(Exception):
    def __init__(
        self,
        message: str,
    ) -> None:
        """
        Base exception for all errors with Lanyard client.

        :param message: Error message.
        """

        self.message: str = message

        super().__init__(self.message)


class KVInvalidError(LanyardError):
    def __init__(self) -> None:
        """
        Exception thrown when the KV body value is not an object (dict)
        """

        super().__init__("Value must be an object (dict)")


class KVValidationError(LanyardError):
    def __init__(self) -> None:
        """
        An exception is thrown when the limits for keys or values in KV are violated.
        """

        super().__init__(
            "Violation of KV limits (https://github.com/Phineas/lanyard?tab=readme-ov-file#limits)"
        )


class NoPermissionError(LanyardError):
    def __init__(self) -> None:
        """
        Exception raised when a user does not have permission to perform the operation.
        """

        super().__init__("You do not have permission to access this resource")


class TokenRequiredError(LanyardError):
    def __init__(self) -> None:
        """
        Exception for methods that require a token to be specified.
        """

        super().__init__("A token must be specified for this request")


class UserNotMonitoredError(LanyardError):
    def __init__(self) -> None:
        """
        Exception when the requested user is not monitored by the service
        """

        super().__init__("User not monitored")


class UnknownAPIVersionError(LanyardError):
    def __init__(self, version: int) -> None:
        """
        Exception for unknown API version

        :param version: API version (default: ``1``).
        """

        self.version: int = version

        super().__init__(f"API version ({self.version}) must be positive integer")


__all__ = [
    "LanyardError",
    "KVInvalidError",
    "NoPermissionError",
    "KVValidationError",
    "TokenRequiredError",
    "UserNotMonitoredError",
    "UnknownAPIVersionError",
]
