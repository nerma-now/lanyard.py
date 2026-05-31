import asyncio
import logging
import sys

from lanyard import HttpxProvider, LanyardClient, LanyardData


async def main() -> None:
    async with LanyardClient(HttpxProvider()) as client:
        data: LanyardData = await client.get_user(338718840873811979)
        print(data["discord_user"]["username"])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
