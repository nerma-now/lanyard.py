from abc import ABC, abstractmethod
from typing import Any


class WsConnection(ABC):
    @abstractmethod
    async def send_json(self, data: Any) -> None: ...

    @abstractmethod
    async def receive_json(self) -> dict[str, Any]: ...

    @abstractmethod
    async def close(self) -> None: ...


__all__ = ["WsConnection"]
