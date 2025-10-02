import asyncio
from contextlib import suppress

from lanyard import LanyardClient, LanyardConfig


async def main() -> None:
    config: LanyardConfig = LanyardConfig(token="TOKEN")

    async with LanyardClient(config=config) as lanyard:
        await lanyard.kv.delete(user_id=988868966179033189, key="lanyard")


if __name__ == "__main__":
    with suppress(KeyboardInterrupt):
        asyncio.run(main())
