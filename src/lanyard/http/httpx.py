from collections.abc import Mapping
from typing import Any, Literal

import httpx

from lanyard.exceptions import LanyardProviderError
from lanyard.loggers import httpx_logger as logger

from .base import HttpProvider, HttpResponse


class HttpxProvider(HttpProvider):
    def __init__(
        self, client: httpx.AsyncClient | None = None, timeout: float | None = None
    ) -> None:
        self._own_client = client is None
        self._client = client or httpx.AsyncClient(timeout=timeout)
        self._timeout = timeout
        logger.info(f"Initialized HttpxProvider (managed_externally={not self._own_client})")

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
                    request_params["content"] = body

            response = await self._client.request(
                method=method,
                url=url,
                headers=headers,
                timeout=timeout if timeout is not None else self._timeout,
                **request_params,
                **kwargs,
            )

            if response.status_code == 204:
                return HttpResponse(status_code=204, body=None)

            try:
                data = response.json()
            except (ValueError, httpx.DecodingError):
                data = response.text

            return HttpResponse(status_code=response.status_code, body=data)

        except httpx.RequestError as ex:
            raise LanyardProviderError(f"HTTPX request error: {ex}") from ex

    async def connect_ws(self, url: str) -> Any:
        raise LanyardProviderError(
            "WebSockets are not supported by HttpxProvider. Please use AiohttpProvider instead."
        )

    async def close(self) -> None:
        if self._own_client:
            logger.info("Closing internal HttpxProvider session")
            await self._client.aclose()
        else:
            logger.debug("Skipping close: client is managed externally")


__all__ = ["HttpxProvider"]
