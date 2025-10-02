from abc import ABC

from .context import ServiceContext


class BaseService(ABC):
    def __init__(self, context: ServiceContext):
        self._context: ServiceContext = context


__all__ = ["BaseService"]
