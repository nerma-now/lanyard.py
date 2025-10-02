from typing import Optional, Dict
from urllib import parse
from pydantic import BaseModel, Field, field_validator

from .constant import API_BASE_URL, API_DEFAULT_VERSION
from .exception import UnknownAPIVersionError


class LanyardConfig(BaseModel):
    """
    Lanyard API client configuration.

    This class contains settings for connecting to the Lanyard API and making management requests.
    """

    base_url: str = Field(default=API_BASE_URL)
    api_version: int = Field(default=API_DEFAULT_VERSION)
    raise_for_status: bool = Field(default=True)
    token: Optional[str] = Field(default=None)
    timeout: Optional[float] = Field(default=None)

    @field_validator("api_version", mode="before")
    @classmethod
    def _validate_api_version(cls, v: int) -> int:
        """
        Validator for converting a dictionary to a list of KeyValueData.

        :param v: Value to convert.

        :return: List of ``KeyValueData``.
        """

        if v is not None and v <= 0:
            raise UnknownAPIVersionError(v)

        return v

    @property
    def url(self) -> str:
        """
        Parses the underlying HTTP link and API version

        :return: HTTP link
        """

        return parse.urljoin(base=self.base_url, url=f"v{self.api_version}/")

    @property
    def headers(self) -> Dict[str, str]:
        """
        Returns a dictionary specifying the content type and user token.

        :return: Return the finished dictionary
        """

        headers: Dict[str, str] = {"Content-Type": "application/json"}

        if self.token is not None:
            headers["Authorization"] = self.token

        return headers


__all__ = ["LanyardConfig"]
