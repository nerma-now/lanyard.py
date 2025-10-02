from types import TracebackType
from typing import Optional, Type, Self

from .service import ServiceContext, UserService, KVService
from .config import LanyardConfig
from .http import BaseHTTP, HTTPX


class LanyardClient:
    def __init__(
        self,
        http: Optional[BaseHTTP] = None,
        config: Optional[LanyardConfig] = None,
    ) -> None:
        """
        The main client class for working with the Lanyard API, implementing an asynchronous context manager.

        :param http: HTTP client for making requests
        :param config: Client configuration
        """

        self.config: LanyardConfig = self._build_config(
            config=config,
        )

        self._http: BaseHTTP = self._build_http_client(
            http=http,
            base_url=self.config.url,
            timeout=self.config.timeout,
            raise_for_status=self.config.raise_for_status,
        )

        self._context: ServiceContext = ServiceContext(
            config=self.config,
            http=self._http,
        )
        self.user: UserService = UserService(
            context=self._context,
        )
        self.kv: KVService = KVService(
            context=self._context,
        )

    @staticmethod
    def _build_config(
        config: Optional[LanyardConfig] = None,
    ) -> LanyardConfig:
        if config is None:
            return LanyardConfig()

        return config

    @staticmethod
    def _build_http_client(
        base_url: str,
        raise_for_status: bool = True,
        http: Optional[BaseHTTP] = None,
        timeout: Optional[float] = None,
    ) -> BaseHTTP:
        if http is not None:
            return http

        return HTTPX(
            base_url=base_url,
            timeout=timeout,
            raise_for_status=raise_for_status,
        )

    async def __aenter__(self) -> Self:
        if hasattr(self._http, "__aenter__"):
            await self._http.__aenter__()

        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        if hasattr(self._http, "__aexit__"):
            await self._http.__aexit__(exc_type, exc_val, exc_tb)


__all__ = ["LanyardClient"]
