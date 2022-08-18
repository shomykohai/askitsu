"""
The MIT License (MIT)

Copyright (c) 2022-present ShomyKohai

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""


from __future__ import annotations

import asyncio
from typing import Any, Dict, Optional


class CacheResult:
    def __init__(self, name: str, value: Any) -> None:
        self.name = name
        self.value = value

    def as_dict(self) -> Dict[str, Any]:
        return {self.name: self.value}

    @property
    def size(self) -> int:
        cache = self.as_dict()
        return cache.__sizeof__()


class Cache:
    def __init__(self, expiration: Optional[int] = None) -> None:
        self.expiration = expiration or 0
        self.__cache: Dict[str, Any] = {}

    async def __remove_after(self, name: str, seconds: int) -> None:
        await asyncio.sleep(seconds)
        await self.remove(name)

    @property
    def size(self) -> int:
        return self.__sizeof__()

    @property
    def cache(self) -> Dict[str, Any]:
        return self.__cache

    async def get(self, name: str) -> Optional[CacheResult]:
        try:
            value = self.__cache[str(name)]
        except (KeyError, TypeError):
            return None
        else:
            return CacheResult(name, value)

    async def add(self, name: str, value: Any, remove_after: int = None) -> CacheResult:
        name = str(name)
        if name in self.__cache:
            return await self.get(name)  # type: ignore
        self.__cache[name] = value
        if remove_after and remove_after > 0:
            asyncio.create_task(self.__remove_after(name, remove_after))
        return CacheResult(name, value)

    async def remove(self, name: str) -> None:
        try:
            self.__cache.pop(str(name))
        except KeyError:
            pass

    async def clear(self) -> None:
        self.__cache = {}
