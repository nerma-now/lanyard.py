import asyncio
import logging
import sys

from lanyard import LanyardClient, LanyardData, HttpxProvider


async def main():
    async with LanyardClient(HttpxProvider()) as client:
        data: LanyardData = await client.get_user(338718840873811979)
        print(data["discord_user"]["username"])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
