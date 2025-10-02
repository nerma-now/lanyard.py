import json

from typing import Optional, Dict, Any

from lanyard.http.exception import NotFoundError
from lanyard.exception import UserNotMonitoredError
from lanyard.decorator import requires_token, handle_error
from lanyard.http import HTTPResponse
from lanyard.model import Response, ResponseData

from .base import BaseService


class UserService(BaseService):
    @handle_error
    async def by_id(self, user_id: int) -> Optional[ResponseData]:
        try:
            response: HTTPResponse = await self._context.http.get(
                path=f"users/{user_id}",
                headers=self._context.config.headers,
            )

            response_json: Dict[str, Any] = json.loads(response.content)
            response_model: Response = Response(**response_json)

            if response_model.data is not None:
                return response_model.data

            return None
        except NotFoundError:
            raise UserNotMonitoredError()

    @requires_token
    @handle_error
    async def me(self) -> Optional[ResponseData]:
        try:
            response: HTTPResponse = await self._context.http.get(
                path="users/@me",
                headers=self._context.config.headers,
            )

            response_json: Dict[str, Any] = json.loads(response.content)
            response_model: Response = Response(**response_json)

            if response_model.data is not None:
                return response_model.data

            return None
        except NotFoundError:
            raise UserNotMonitoredError()


__all__ = ["UserService"]
