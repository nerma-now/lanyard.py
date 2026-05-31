import asyncio
from collections.abc import Callable, Coroutine
from functools import wraps
from typing import Any

from lanyard.exceptions import LanyardProviderError, LanyardUnauthorizedError
from lanyard.loggers import logger

type AsyncFunc[**P, R] = Callable[P, Coroutine[Any, Any, R]]


def authorized[**P, R](func: AsyncFunc[P, R]) -> AsyncFunc[P, R]:
    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        instance: Any = args[0]
        token = kwargs.get("token") or getattr(instance, "_token", None)

        if not token:
            raise LanyardUnauthorizedError()
        return await func(*args, **kwargs)

    return wrapper


def retry(
    attempts: int | None = None, delay: float | None = None
) -> Callable[[AsyncFunc[Any, Any]], AsyncFunc[Any, Any]]:
    def decorator[**P, R](func: AsyncFunc[P, R]) -> AsyncFunc[P, R]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            instance: Any = args[0]

            max_attempts = getattr(instance, "_retry_attempts", attempts or 3)
            wait_delay = getattr(instance, "_retry_delay", delay or 1.0)

            last_error: Exception | None = None

            for i in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except LanyardProviderError as ex:
                    last_error = ex
                    if i < max_attempts - 1:
                        logger.warning(
                            f"Retry {i + 1}/{max_attempts} after error: {ex}. "
                            f"Waiting {wait_delay}s..."
                        )
                        await asyncio.sleep(wait_delay)

            logger.error(f"Request failed after {max_attempts} attempts.")
            raise last_error or LanyardProviderError("Maximum retry attempts reached")

        return wrapper

    return decorator


__all__ = ["authorized", "retry"]
