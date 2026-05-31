from typing import Any


class LanyardError(Exception):
    code: str = "lanyard_error"
    message: str = "An unexpected error occurred"

    def __init__(
        self,
        message: str | None = None,
        code: str | None = None,
        payload: dict[str, Any] | None = None,
    ) -> None:
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code
        self.payload = payload or {}
        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message


class LanyardAPIError(LanyardError):
    code: str = "api_error"
    message: str = "Unknown API error"

    def __init__(
        self,
        message: str | None = None,
        code: str | None = None,
        *,
        status_code: int,
        method: str,
        url: str,
        body: Any | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        payload: dict[str, Any] | None = None,
    ):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

        self.status_code = status_code
        self.method = method
        self.url = url
        self.body = body
        self.params = params
        self.headers = headers

        full_message = (
            f"Request to Lanyard API ({method} {url}) returned status_code: {status_code}"
        )
        super().__init__(message=full_message, code=code, payload=payload)


class LanyardSocketError(LanyardError):
    code: str = "socket_error"


class LanyardSocketCloseError(LanyardSocketError):
    def __init__(self, code: int, message: str):
        self.close_code = code
        error_map: dict[int, str] = {
            4004: "unknown_opcode",
            4005: "requires_data_object",
            4006: "invalid_payload",
        }
        super().__init__(
            message=f"Socket closed with code {code} ({error_map.get(code, 'unknown')})",
            payload={"close_code": code, "api_message": message},
        )


class LanyardProviderError(LanyardError):
    code: str = "provider_error"


class LanyardUnauthorizedError(LanyardError):
    code: str = "unauthorized"
    message: str = "Invalid or missing authorization token"


__all__ = [
    "LanyardAPIError",
    "LanyardError",
    "LanyardProviderError",
    "LanyardSocketCloseError",
    "LanyardSocketError",
    "LanyardUnauthorizedError",
]
