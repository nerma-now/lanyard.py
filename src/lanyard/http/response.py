from pydantic import BaseModel, Field


class HTTPResponse(BaseModel):
    """
    Model for a standardized HTTP response.
    """

    method: str = Field(...)
    url: str = Field(...)
    status_code: int = Field(...)
    content: bytes = Field(...)


__all__ = ["HTTPResponse"]
