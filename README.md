<div align=center>

[![Lanyard.py](https://raw.githubusercontent.com/nerma-now/lanyard.py/master/assets/banner.png)](https://github.com/nerma-now/lanyard.py)

<p><b>lanyard.py is a modern and fully asynchronous wrapper for Lanyard API (REST & WebSocket) written in Python 3.12+.</b></p>

[![PyPI - Version](https://img.shields.io/pypi/v/lanyard-py?style=flat-square)](https://pypi.org/project/lanyard-py/)
[![GitHub License](https://img.shields.io/github/license/nerma-now/lanyard.py?style=flat-square)](https://github.com/nerma-now/lanyard.py/blob/master/LICENSE)
[![GitHub contributors](https://img.shields.io/github/contributors/nerma-now/lanyard.py?style=flat-square)](https://github.com/nerma-now/lanyard.py/graphs/contributors)

</div>

---

## Installation

```bash
# Install with httpx support
pip install "lanyard.py[httpx]"
# or (To work with WebSocket, select aiohttp)
pip install "lanyard.py[aiohttp]"
```

## Quick Start

### REST API
```python
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
```

### WebSocket
```python
import asyncio
import logging
import sys

from lanyard import LanyardClient, AiohttpProvider


async def main():
    async with LanyardClient(AiohttpProvider()) as client:
        async for data in client.subscribe(338718840873811979):
            print(data["discord_user"]["username"])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
```

## Available Methods

### REST
| Method | Description | Auth Required |
| :--- | :--- | :---: |
| `get_user(user_id)` | Retrieve presence data for a specific user. | No |
| `get_me()` | Retrieve presence data for the authenticated user. | Yes |
| `set_kv(user_id, key, value)` | Set a single key-value pair in Lanyard KV. | Yes |
| `update_kv(user_id, data)` | Bulk update/merge multiple KV pairs. | Yes |
| `delete_kv(user_id, key)` | Delete a key from Lanyard KV. | Yes |

### WebSocket
| Method | Description |
| :--- | :--- |
| `subscribe(*user_ids)` | Subscribe to one or more user IDs. |
| `subscribe(subscribe_to_all=True)` | Subscribe to all users monitored by Lanyard. |

## Error Handling

The library uses a hierarchy of exceptions for granular error management:

- `LanyardError`: Base exception for all library-related errors.
- `LanyardAPIError`: Raised when the API returns an error or a non-200 status code.
- `LanyardProviderError`: Raised for network-related issues (timeouts, connection failures).
- `LanyardUnauthorizedError`: Raised when a token is missing or invalid.
- `LanyardSocketError`: Base class for WebSocket-related errors.
- `LanyardSocketCloseError`: Raised when the server closes the WebSocket with a specific error code.

## Examples

Detailed implementation examples are available in the [example/](https://github.com/nerma-now/lanyard.py/tree/master/examples) directory:
- Basic REST usage
- Real-time monitoring via WebSockets

---

<div align=center>
Made with ❤️ in Python
</div>
