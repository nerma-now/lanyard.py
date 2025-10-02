import asyncio
from contextlib import suppress

from typing import Optional

from lanyard import LanyardClient, LanyardConfig
from lanyard.model import ResponseData


async def main() -> None:
    config: LanyardConfig = LanyardConfig(token="TOKEN")

    async with LanyardClient(config=config) as lanyard:
        response: Optional[ResponseData] = await lanyard.user.me()

        if response is not None:
            print(response)


if __name__ == "__main__":
    with suppress(KeyboardInterrupt):
        asyncio.run(main())
