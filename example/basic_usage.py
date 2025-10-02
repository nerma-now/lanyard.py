import asyncio

from typing import Optional

from lanyard import LanyardClient
from lanyard.model import ResponseData


async def main() -> None:
    async with LanyardClient() as lanyard:
        response: Optional[ResponseData] = await lanyard.user.by_id(988868966179033189)

        if response is not None:
            print(response)


if __name__ == "__main__":
    asyncio.run(main())
