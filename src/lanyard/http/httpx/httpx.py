from types import TracebackType
from typing import Optional, Self, Type, Any

from httpx import AsyncClient, Response

from lanyard.http.base import BaseHTTP
from lanyard.http.response import HTTPResponse
from lanyard.http.exception import HTTPError

from .exception import ContextRequiredError


# TODO: Requires write description for this code


class HTTPX(BaseHTTP):
    def __init__(
        self,
        base_url: str,
        raise_for_status: bool = True,
        timeout: Optional[float] = None,
    ) -> None:
        self.base_url: str = base_url
        self.raise_for_status: bool = raise_for_status
        self.timeout: Optional[float] = timeout

        self._session: Optional[AsyncClient] = None

        super().__init__(
            base_url=self.base_url,
            raise_for_status=self.raise_for_status,
            timeout=self.timeout,
        )

    async def __aenter__(self) -> Self:
        if self._session is None:
            self._session = AsyncClient(
                base_url=self.base_url,
                timeout=self.timeout,
            )

        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        if self._session is not None:
            await self._session.aclose()

    @property
    def session(self) -> AsyncClient:
        if not self._session:
            raise ContextRequiredError()

        return self._session

    async def _request(
        self,
        method: str,
        url: str,
        **kwargs: Any,
    ) -> HTTPResponse:
        try:
            response: Response = await self.session.request(
                method=method,
                url=url,
                **kwargs,
            )

            return HTTPResponse(
                method=method,
                url=url,
                status_code=response.status_code,
                content=response.content,
            )
        except Exception as exc:
            raise HTTPError(
                method=method,
                url=url,
                message=str(exc),
            )


__all__ = ["HTTPX"]
