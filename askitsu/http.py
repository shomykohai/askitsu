import aiohttp
from typing import Any, Optional
from . import __version__
from .error import BadApiRequest, HTTPError, NotAuthenticated, NotFound


class HTTPClient:

    BASE: str = "https://kitsu.io/api/edge/"

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

    async def get_data(self, url: str) -> Any:
        async with self.__session.get(
            url=f"{self.BASE}{url}", headers=self.__headers
        ) as response:
            response_data = await response.json()
            if response.status == 200:
                return response_data
            if response.status == 404:
                raise NotFound
            if response.status == 401:
                raise NotAuthenticated
            if response.status == 400:
                raise BadApiRequest(response_data["errors"][0])

    async def close(self) -> None:
        return await self.__session.close()
