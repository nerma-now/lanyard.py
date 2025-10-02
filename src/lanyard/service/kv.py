import json

from typing import Dict, Any

from lanyard.http.exception import NotFoundError
from lanyard.exception import KVValidationError, KVInvalidError
from lanyard.decorator import requires_token, handle_error

from .base import BaseService


class KVService(BaseService):
    @requires_token
    @handle_error
    async def set(self, user_id: int, key: str, value: str) -> None:
        try:
            await self._context.http.put(
                path=f"users/{user_id}/kv/{key}",
                headers=self._context.config.headers,
                data=value,
            )

            return None
        except NotFoundError:
            raise KVValidationError()

    @requires_token
    @handle_error
    async def delete(self, user_id: int, key: str) -> None:
        try:
            await self._context.http.delete(
                path=f"users/{user_id}/kv/{key}",
                headers=self._context.config.headers,
            )

            return None
        except NotFoundError:
            raise KVValidationError()

    @requires_token
    @handle_error
    async def merge(self, user_id: int, value: Dict[str, Any]) -> None:
        if not isinstance(value, dict):
            raise KVInvalidError()

        try:
            await self._context.http.patch(
                path=f"users/{user_id}/kv",
                headers=self._context.config.headers,
                data=json.dumps(value),
            )

            return None
        except NotFoundError:
            raise KVValidationError()


__all__ = ["KVService"]
