from enum import IntEnum


class Opcode(IntEnum):
    EVENT = 0
    HELLO = 1
    INITIALIZE = 2
    HEARTBEAT = 3


__all__ = ["Opcode"]
