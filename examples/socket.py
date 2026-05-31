import asyncio
import logging
import sys

from lanyard import AiohttpProvider, LanyardClient


async def main() -> None:
    async with LanyardClient(AiohttpProvider()) as client:
        async for data in client.subscribe(988868966179033189):
            print(data["discord_user"]["username"])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
