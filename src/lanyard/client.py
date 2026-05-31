import asyncio
from collections.abc import AsyncGenerator
from typing import Any, Final, Literal, Self, cast
from urllib.parse import urljoin

from lanyard.decorators import authorized, retry
from lanyard.enums import Opcode
from lanyard.exceptions import (
    LanyardAPIError,
    LanyardProviderError,
    LanyardSocketCloseError,
    LanyardSocketError,
    LanyardUnauthorizedError,
)
from lanyard.http import HttpProvider
from lanyard.loggers import logger
from lanyard.models import LanyardData


class LanyardClient:
    """
    Main client for interacting with the Lanyard API (REST and WebSocket).
    """

    DEFAULT_BASE_URL: Final[str] = "https://api.lanyard.rest"
    DEFAULT_WS_URL: Final[str] = "wss://api.lanyard.rest/socket"

    def __init__(
        self,
        provider: HttpProvider,
        *,
        base_url: str | None = None,
        token: str | None = None,
        version: str = "v1",
        retry_attempts: int = 3,
        retry_delay: float = 1.0,
        ws_url: str | None = None,
    ) -> None:
        """
        Initialize the Lanyard client.

        :param provider: The HTTP provider to use for requests (e.g., HttpxProvider).
        :param base_url: Optional custom base URL for the REST API.
        :param token: Optional API key for authorized requests.
        :param version: API version to use. Defaults to "v1".
        :param retry_attempts: Number of times to retry failed network requests.
        :param retry_delay: Seconds to wait between retry attempts.
        :param ws_url: Optional custom URL for the WebSocket connection.
        """
        self._provider = provider
        self._token = token

        root_url: str = base_url or self.DEFAULT_BASE_URL
        if not root_url.endswith("/"):
            root_url += "/"

        self._base_path: str = urljoin(root_url, f"{version}/")

        self._retry_attempts = retry_attempts
        self._retry_delay = retry_delay
        self._ws_url = ws_url or self.DEFAULT_WS_URL
        logger.info(f"Initialized LanyardClient (version: {version}, retries: {retry_attempts})")

    def _build_url(self, endpoint: str) -> str:
        """
        Build a complete URL for a given API endpoint.

        :param endpoint: The API path (e.g., 'users/ID').
        :return: A full URL string.
        """
        return urljoin(self._base_path, endpoint.lstrip("/"))

    @retry()
    async def _request(
        self,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH"],
        endpoint: str,
        *,
        token: str | None = None,
        body: Any = None,
    ) -> Any:
        """
        Perform an internal HTTP request with error handling and retries.

        :param method: HTTP method to use.
        :param endpoint: The API endpoint to call.
        :param token: Optional token to override the default client token.
        :param body: Optional JSON-serializable body for the request.
        :return: The 'data' field from the API response.
        :raises LanyardUnauthorizedError: If no valid token is provided for authorized routes.
        :raises LanyardAPIError: If the API returns an error or failure status.
        """
        url = self._build_url(endpoint)
        logger.debug(f"Sending {method} request to {url}")

        headers: dict[str, str] = {}

        if body is not None:
            headers["Content-Type"] = "application/json"

        auth = token or self._token
        if auth:
            headers["Authorization"] = auth.strip()

        response = await self._provider.request(
            method=method,
            url=url,
            headers=headers,
            body=body,
        )

        status = response.status_code
        data = response.body

        if status in (401, 403):
            logger.error(f"Unauthorized access to {url} (status: {status})")
            raise LanyardUnauthorizedError()

        is_success = isinstance(data, dict) and data.get("success") is True
        if status >= 400 or not is_success:
            error_info = data.get("error", {}) if isinstance(data, dict) else {}
            logger.warning(
                f"API Error at {method} {url}: status {status}, code: {error_info.get('code')}"
            )
            raise LanyardAPIError(
                message=error_info.get("message") or str(data),
                code=error_info.get("code"),
                status_code=status,
                method=method,
                url=url,
                body=body,
                headers=headers,
                payload=error_info if isinstance(data, dict) else None,
            )

        logger.debug(f"Successfully received data from {url}")
        return data.get("data") if isinstance(data, dict) else data

    async def get_user(self, user_id: str | int) -> LanyardData:
        """
        Retrieve presence data for a specific user.

        :param user_id: The Discord Snowflake ID of the user.
        :return: A LanyardData dictionary containing user status and activities.
        """
        return cast("LanyardData", await self._request("GET", f"users/{user_id}"))

    @authorized
    async def get_me(self, *, token: str | None = None) -> LanyardData:
        """
        Retrieve presence data for the authenticated user (requires token).

        :param token: Optional token to use for this specific request.
        :return: A LanyardData dictionary for the authorized account.
        """
        return cast("LanyardData", await self._request("GET", "users/@me", token=token))

    @authorized
    async def set_kv(
        self, user_id: str | int, key: str, value: Any, *, token: str | None = None
    ) -> None:
        """
        Set a single key-value pair in the user's Lanyard KV store.

        :param user_id: The Discord Snowflake ID of the user.
        :param key: The key to set (alphanumeric).
        :param value: The value to store.
        :param token: Optional token to use for this specific request.
        """
        await self._request("PUT", f"users/{user_id}/kv/{key}", token=token, body=value)

    @authorized
    async def delete_kv(self, user_id: str | int, key: str, *, token: str | None = None) -> None:
        """
        Remove a key from the user's Lanyard KV store.

        :param user_id: The Discord Snowflake ID of the user.
        :param key: The key to delete.
        :param token: Optional token to use for this specific request.
        """
        await self._request("DELETE", f"users/{user_id}/kv/{key}", token=token)

    @authorized
    async def update_kv(
        self, user_id: str | int, data: dict[str, Any], *, token: str | None = None
    ) -> None:
        """
        Update multiple key-value pairs at once (merges with existing store).

        :param user_id: The Discord Snowflake ID of the user.
        :param data: A dictionary of key-value pairs to update.
        :param token: Optional token to use for this specific request.
        """
        payload = {str(k): str(v) for k, v in data.items()}
        await self._request("PATCH", f"users/{user_id}/kv", token=token, body=payload)

    async def subscribe(
        self, *user_ids: str | int, subscribe_to_all: bool = False
    ) -> AsyncGenerator[LanyardData, None]:
        """
        Subscribe to real-time status updates via WebSocket.

        :param user_ids: One or more Discord Snowflake IDs to monitor.
        :param subscribe_to_all: If True, subscribe to updates for all users monitored by Lanyard.
        :yields: LanyardData dictionaries as presence updates occur.
        :raises LanyardProviderError: If the WebSocket connection fails to initialize.
        :raises LanyardSocketError: If the connection is lost.
        :raises LanyardSocketCloseError: If the server closes the socket with a specific error code.
        """
        ws = await self._provider.connect_ws(self._ws_url)
        heartbeat_task: asyncio.Task[None] | None = None

        try:
            try:
                hello = await ws.receive_json()
            except Exception as e:
                raise LanyardProviderError(f"Failed to connect to WebSocket: {e}") from e

            if hello.get("op") != Opcode.HELLO:
                raise LanyardSocketError(f"Expected Hello (Op 1), got {hello.get('op')}")

            interval = hello["d"]["heartbeat_interval"] / 1000

            async def heartbeat() -> None:
                while True:
                    await asyncio.sleep(interval)
                    await ws.send_json({"op": Opcode.HEARTBEAT})

            heartbeat_task = asyncio.create_task(heartbeat())

            init_data: dict[str, Any] = {}
            if subscribe_to_all:
                init_data["subscribe_to_all"] = True
            elif len(user_ids) == 1:
                init_data["subscribe_to_id"] = str(user_ids[0])
            else:
                init_data["subscribe_to_ids"] = [str(uid) for uid in user_ids]

            await ws.send_json({"op": Opcode.INITIALIZE, "d": init_data})

            while True:
                try:
                    msg = await ws.receive_json()
                except Exception as ex:
                    close_code = getattr(ex, "code", None)
                    if isinstance(close_code, int) and close_code >= 4000:
                        raise LanyardSocketCloseError(close_code, str(ex)) from ex
                    raise LanyardSocketError(f"WebSocket connection lost: {ex}") from ex

                op, event, d = msg.get("op"), msg.get("t"), msg.get("d")

                if op == Opcode.EVENT:
                    if event == "INIT_STATE":
                        if isinstance(d, dict) and "discord_user" not in d:
                            for user_data in d.values():
                                yield cast("LanyardData", user_data)
                        else:
                            yield cast("LanyardData", d)
                    elif event == "PRESENCE_UPDATE":
                        yield cast("LanyardData", d)
        finally:
            if heartbeat_task:
                heartbeat_task.cancel()
            await ws.close()

    async def close(self) -> None:
        """
        Shutdown the client and close the underlying provider session.
        """
        logger.info("Closing LanyardClient provider...")
        await self._provider.close()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()


__all__ = ["LanyardClient"]
