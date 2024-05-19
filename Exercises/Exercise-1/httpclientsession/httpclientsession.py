import aiohttp, aiofiles
import traceback
import sys
import os
from typing import Optional
from types import TracebackType


class AioHttpSession:
    def __init__(self) -> None:
        self._session = aiohttp.ClientSession()

    async def __aenter__(self) -> "MyClass":
        return self

    async def __aexit__(
        self,
        exc_type: type,
        exc_val: Exception,
        traceback: Optional[TracebackType]
    ) -> None:
        await self.close()

    async def close(self) -> None:
        await self._session.close()

    async def download_file(self, url: str, dest: str) -> str:
        file_name = url.split('/')[-1]
        chunk_size = 16384
        dest_file = os.path.join(dest, file_name)
        async with self._session.get(url) as response:
            async with aiofiles.open(dest_file, mode="wb") as f:
                async for data in response.content.iter_chunked(chunk_size):
                    await f.write(data)
        return dest_file
