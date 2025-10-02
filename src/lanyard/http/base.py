from abc import ABC, abstractmethod
from urllib import parse
from typing import Optional, Any

from .type import Headers, Params, Data
from .decorator import handle_http_error
from .response import HTTPResponse


class BaseHTTP(ABC):
    def __init__(
        self,
        base_url: str,
        raise_for_status: bool = True,
        timeout: Optional[float] = None,
    ) -> None:
        """
        The base abstract class for all HTTP-related classes.

        :param base_url: Base URL of HTTP response (example: ``https://api.lanyard.rest/``).
        :param raise_for_status: Raise HTTP status code of HTTP response (example: ``True``).
        :param timeout: Timeout for HTTP requests (example: ``None``).
        """

        self.base_url: str = base_url
        self.raise_for_status: bool = raise_for_status
        self.timeout: Optional[float] = timeout

    @staticmethod
    def _build_url(base_url: str, path: Optional[str]) -> str:
        if path is None:
            return base_url

        return parse.urljoin(base_url, path)

    @abstractmethod
    async def _request(self, method: str, url: str, **kwargs: Any) -> HTTPResponse:
        raise NotImplementedError()

    @handle_http_error
    async def get(
        self,
        path: Optional[str] = None,
        params: Optional[Params] = None,
        headers: Optional[Headers] = None,
        **kwargs: Any,
    ) -> HTTPResponse:
        """
        Executes an async HTTP GET request.

        :param path: URL for request.
        :param params: Query parameters to include in the URL.
        :param headers: Headers to include in the request.
        :param kwargs: Additional fields for HTTP client attributes.
        """

        url: str = self._build_url(
            base_url=self.base_url,
            path=path,
        )

        return await self._request(
            method="GET",
            url=url,
            params=params,
            headers=headers,
            **kwargs,
        )

    @handle_http_error
    async def put(
        self,
        path: Optional[str] = None,
        data: Optional[Data] = None,
        params: Optional[Params] = None,
        headers: Optional[Headers] = None,
        **kwargs: Any,
    ) -> HTTPResponse:
        """
        Executes an async HTTP PUT request.

        :param path: URL for request.
        :param data: Body of request to include in the request.
        :param params: Query parameters to include in the URL.
        :param headers: Headers to include in the request.
        :param kwargs: Additional fields for HTTP client attributes.
        """

        url: str = self._build_url(
            base_url=self.base_url,
            path=path,
        )

        return await self._request(
            method="PUT",
            url=url,
            data=data,
            params=params,
            headers=headers,
            **kwargs,
        )

    @handle_http_error
    async def patch(
        self,
        path: Optional[str] = None,
        data: Optional[Data] = None,
        params: Optional[Params] = None,
        headers: Optional[Headers] = None,
        **kwargs: Any,
    ) -> HTTPResponse:
        """
        Executes an async HTTP PATCH request.

        :param path: URL for request.
        :param data: Body of request to include in the request.
        :param params: Query parameters to include in the URL.
        :param headers: Headers to include in the request.
        :param kwargs: Additional fields for HTTP client attributes.
        """

        url: str = self._build_url(
            base_url=self.base_url,
            path=path,
        )

        return await self._request(
            method="PATCH",
            url=url,
            data=data,
            params=params,
            headers=headers,
            **kwargs,
        )

    @handle_http_error
    async def delete(
        self,
        path: Optional[str] = None,
        params: Optional[Params] = None,
        headers: Optional[Headers] = None,
        **kwargs: Any,
    ) -> HTTPResponse:
        """
        Executes an async HTTP DELETE request.

        :param path: URL for request.
        :param params: Query parameters to include in the URL.
        :param headers: Headers to include in the request.
        :param kwargs: Additional fields for HTTP client attributes.
        """

        url: str = self._build_url(
            base_url=self.base_url,
            path=path,
        )

        return await self._request(
            method="DELETE",
            url=url,
            params=params,
            headers=headers,
            **kwargs,
        )


__all__ = ["BaseHTTP"]
