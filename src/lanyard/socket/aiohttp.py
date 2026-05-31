from typing import Any

import aiohttp

from .base import WsConnection


class AiohttpWsConnection(WsConnection):
    def __init__(self, ws: aiohttp.ClientWebSocketResponse) -> None:
        self._ws = ws

    async def send_json(self, data: Any) -> None:
        await self._ws.send_json(data)

    async def receive_json(self) -> dict[str, Any]:
        data: dict[str, Any] = await self._ws.receive_json()
        return data

    async def close(self) -> None:
        await self._ws.close()


__all__ = ["AiohttpWsConnection"]
