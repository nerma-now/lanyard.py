from abc import ABC, abstractmethod
from collections.abc import Mapping
from dataclasses import dataclass
from types import TracebackType
from typing import Any, Literal

from lanyard.socket import WsConnection


@dataclass(frozen=True)
class HttpResponse[T: Any]:
    status_code: int
    body: T


class HttpProvider(ABC):
    @abstractmethod
    async def request(
        self,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH"],
        url: str,
        *,
        headers: Mapping[str, str] | None = None,
        body: Any = None,
        timeout: float | None = None,
        **kwargs: Any,
    ) -> HttpResponse[Any]: ...

    @abstractmethod
    async def connect_ws(self, url: str) -> WsConnection: ...

    @abstractmethod
    async def close(self) -> None: ...

    async def __aenter__(self) -> "HttpProvider":
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.close()


__all__ = ["HttpProvider", "HttpResponse"]
