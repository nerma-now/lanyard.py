from enum import StrEnum


class DiscordStatus(StrEnum):
    """
    Discord user statuses.
    """

    ONLINE = "online"
    OFFLINE = "offline"
    DND = "dnd"
    IDLE = "idle"


__all__ = ["DiscordStatus"]
