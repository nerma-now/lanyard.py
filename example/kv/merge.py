import asyncio
from contextlib import suppress

from lanyard import LanyardClient, LanyardConfig


async def main() -> None:
    config: LanyardConfig = LanyardConfig(token="TOKEN")

    async with LanyardClient(config=config) as lanyard:
        await lanyard.kv.merge(user_id=988868966179033189, value={"lanyard": "py"})


if __name__ == "__main__":
    with suppress(KeyboardInterrupt):
        asyncio.run(main())
