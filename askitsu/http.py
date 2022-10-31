import aiohttp
from typing import Any, Optional
from . import __version__
from .error import HTTPError


__all__ = ("HTTPClient",)


class HTTPClient:

    def __init__(self, session: aiohttp.ClientSession, token: str = None) -> None:
        self.__authorization = f"Bearer {token}" if token else ""
        self.__session = session
        self.__headers = {
            "Accept": "application/vnd.api+json",
            "Content-Type": "application/vnd.api+json",
            "User-Agent": f"askitsu (https://github.com/ShomyKohai/askitsu {__version__})",
            "Authorization": self.__authorization,
        }
        self.token: Optional[str] = token

    @property
    def session(self) -> aiohttp.ClientSession:
        return self.__session

    async def post_data(self, data: dict) -> Any:
        async with self.__session.post(
            url="https://kitsu.io/api/graphql",
            json=data,
            headers=self.__headers
        ) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise HTTPError("Something went wrong.", response.status)

    async def close(self) -> None:
        return await self.__session.close()