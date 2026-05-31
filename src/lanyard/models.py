from typing import Any, TypedDict

type Snowflake = str


class AvatarDecorationData(TypedDict, total=False):
    asset: str
    sku_id: Snowflake
    expires_at: int | None


class PrimaryGuildData(TypedDict, total=False):
    identity_guild_id: Snowflake | None
    identity_enabled: bool | None
    tag: str | None
    badge: str | None


class DiscordUser(TypedDict, total=False):
    id: Snowflake
    username: str
    discriminator: str
    global_name: str | None
    display_name: str | None
    avatar: str | None
    bot: bool
    public_flags: int
    avatar_decoration_data: AvatarDecorationData | None
    primary_guild: PrimaryGuildData | None
    display_name_styles: dict[str, Any] | None


class TimestampData(TypedDict, total=False):
    start: int | None
    end: int | None


class AssetData(TypedDict, total=False):
    large_image: str | None
    large_text: str | None
    large_url: str | None
    small_image: str | None
    small_text: str | None
    small_url: str | None


class ActivityData(TypedDict, total=False):
    id: Snowflake
    type: int
    name: str
    created_at: int
    platform: str | None
    application_id: Snowflake | None
    sync_id: Snowflake | None
    session_id: Snowflake | None
    flags: int | None
    state: str | None
    details: str | None
    timestamps: TimestampData | None
    assets: AssetData | None


class SpotifyData(TypedDict, total=False):
    album: str | None
    album_art_url: str | None
    artist: str | None
    song: str | None
    track_id: Snowflake | None
    timestamps: TimestampData | None


class LanyardData(TypedDict, total=False):
    discord_user: DiscordUser
    kv: dict[str, str]
    listening_to_spotify: bool
    active_on_discord_embedded: bool
    active_on_discord_mobile: bool
    active_on_discord_desktop: bool
    active_on_discord_web: bool
    active_on_discord_vr: bool
    activities: list[ActivityData]
    discord_status: str
    spotify: SpotifyData | None


__all__ = ["ActivityData", "DiscordUser", "LanyardData", "SpotifyData"]
