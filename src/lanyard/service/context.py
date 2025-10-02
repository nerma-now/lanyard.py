from __future__ import annotations

from typing import TYPE_CHECKING, Any
from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from lanyard.http import BaseHTTP
    from lanyard.rest import LanyardConfig


class ServiceContext(BaseModel):
    http: Any = Field(...)
    config: Any = Field(...)

    def __init__(self, http: BaseHTTP, config: LanyardConfig):
        super().__init__(http=http, config=config)


__all__ = ["ServiceContext"]
