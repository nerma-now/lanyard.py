from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal

if TYPE_CHECKING:
    import aiohttp
else:
    try:
        import aiohttp
    except ImportError:
        httpx = None

from lanyard.exceptions import LanyardProviderError
from lanyard.loggers import aiohttp_logger as logger
from lanyard.socket import AiohttpWsConnection, WsConnection

from .base import HttpProvider, HttpResponse


class AiohttpProvider(HttpProvider):
    def __init__(
        self,
        session: aiohttp.ClientSession | None = None,
        timeout: float | None = None,
    ) -> None:
        self._own_session = session is None
        self._session = session or aiohttp.ClientSession()
        self._timeout = timeout
        logger.info(f"Initialized AiohttpProvider (managed_externally={not self._own_session})")

    def _get_session(self) -> aiohttp.ClientSession:
        if self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def request(
        self,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH"],
        url: str,
        *,
        headers: Mapping[str, str] | None = None,
        body: Any = None,
        timeout: float | None = None,
        **kwargs: Any,
    ) -> HttpResponse[Any]:
        try:
            request_params: dict[str, Any] = {}
            if body is not None:
                if isinstance(body, (dict, list)):
                    request_params["json"] = body
                else:
                    request_params["data"] = body

            timeout_value = timeout if timeout is not None else self._timeout
            aiohttp_timeout = aiohttp.ClientTimeout(total=timeout_value) if timeout_value else None

            session = self._get_session()

            async with session.request(
                method=method,
                url=url,
                headers=headers,
                timeout=aiohttp_timeout,
                **request_params,
                **kwargs,
            ) as response:
                if response.status == 204:
                    return HttpResponse(status_code=204, body=None)

                try:
                    data = await response.json()
                except (aiohttp.ContentTypeError, ValueError):
                    data = await response.text()

                return HttpResponse(status_code=response.status, body=data)

        except aiohttp.ClientError as ex:
            raise LanyardProviderError(f"Aiohttp request error: {ex}") from ex

    async def connect_ws(self, url: str) -> WsConnection:
        try:
            session = self._get_session()
            ws = await session.ws_connect(url)
            return AiohttpWsConnection(ws)
        except aiohttp.ClientError as ex:
            raise LanyardProviderError(f"Aiohttp WebSocket connection error: {ex}") from ex

    async def close(self) -> None:
        if self._own_session:
            logger.info("Closing internal AiohttpProvider session")
            await self._session.close()
        else:
            logger.debug("Skipping close: session is managed externally")


__all__ = ["AiohttpProvider"]
