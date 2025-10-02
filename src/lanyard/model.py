from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, List, Dict, Any

from .type import Snowflake
from .enum import DiscordStatus


class AvatarDecorationData(BaseModel):
    """
    Data model for decorating the avatar of a Discord user.
    """

    asset: str = Field(...)
    sku_id: Snowflake = Field(...)


class PrimaryGuildData(BaseModel):
    """
    Data model of the user's main server (guild).
    """

    identity_guild_id: Optional[Snowflake] = Field(default=None)
    identity_enabled: Optional[bool] = Field(default=None)
    tag: Optional[str] = Field(default=None)
    badge: Optional[str] = Field(default=None)


class DiscordUser(BaseModel):
    """
    The basic user model of Discord.
    """

    id: Snowflake = Field(...)
    username: str = Field(...)
    discriminator: str = Field(...)
    bot: bool = Field(...)
    public_flags: int = Field(...)
    global_name: Optional[str] = Field(default=None)
    avatar: Optional[str] = Field(default=None)
    avatar_decoration_data: Optional[AvatarDecorationData] = Field(default=None)
    primary_guild: Optional[PrimaryGuildData] = Field(default=None)


class KeyValueData(BaseModel):
    """
    A model for storing key-value pairs.
    """

    key: str = Field(...)
    value: str = Field(...)


class TimestampData(BaseModel):
    """
    Timestamp model.
    """

    start: Optional[datetime] = Field(default=None)
    end: Optional[datetime] = Field(default=None)


class AssetData(BaseModel):
    """
    Activity resource (image) data model.
    """

    large_image: Optional[str] = Field(default=None)
    large_text: Optional[str] = Field(default=None)
    large_url: Optional[str] = Field(default=None)
    small_image: Optional[str] = Field(default=None)
    small_text: Optional[str] = Field(default=None)
    small_url: Optional[str] = Field(default=None)


class ActivityData(BaseModel):
    """
    Discord user activity data model.
    """

    id: Snowflake = Field(...)
    type: int = Field(...)
    created_at: datetime = Field(...)
    application_id: Optional[Snowflake] = Field(default=None)
    sync_id: Optional[Snowflake] = Field(default=None)
    session_id: Optional[Snowflake] = Field(default=None)
    flags: Optional[int] = Field(default=None)
    state: Optional[str] = Field(default=None)
    details: Optional[str] = Field(default=None)
    timestamps: Optional[TimestampData] = Field(default=None)
    assets: Optional[AssetData] = Field(default=None)


class SpotifyData(BaseModel):
    """
    Spotify Activity Data Model.
    """

    timestamps: Optional[TimestampData] = Field(default=None)
    album: Optional[str] = Field(default=None)
    album_art_url: Optional[str] = Field(default=None)
    artist: Optional[str] = Field(default=None)
    song: Optional[str] = Field(default=None)
    track_id: Optional[Snowflake] = Field(default=None)


class ResponseData(BaseModel):
    """
    The basic data model of a response with user status information.
    """

    discord_user: DiscordUser = Field(...)
    kv: List[KeyValueData] = Field(...)
    listening_to_spotify: bool = Field(...)
    active_on_discord_embedded: bool = Field(...)
    active_on_discord_mobile: bool = Field(...)
    active_on_discord_desktop: bool = Field(...)
    active_on_discord_web: bool = Field(...)
    activities: List[ActivityData] = Field(...)
    discord_status: DiscordStatus = Field(...)
    spotify: Optional[SpotifyData] = Field(default=None)

    @field_validator("kv", mode="before")
    @classmethod
    def _validate_kv(cls, v: Dict[str, Any]) -> List[KeyValueData]:
        """
        Validator for converting a dictionary to a list of KeyValueData.

        :param v: Value to convert.
        :return: List of ``KeyValueData``.
        """

        return [KeyValueData(key=key, value=value) for key, value in v.items()]


class ResponseError(BaseModel):
    """
    Response error model.
    """

    code: str = Field(...)
    message: str = Field(...)


class Response(BaseModel):
    """
    Basic API response model.
    """

    success: bool = Field(...)
    data: Optional[ResponseData] = Field(default=None)
    error: Optional[ResponseError] = Field(default=None)


__all__ = [
    "Response",
    "ResponseData",
    "ResponseError",
]
