from __future__ import annotations

import aiohttp
import logging
from typing import Any, List, Optional, overload, TYPE_CHECKING, Union
from . import __version__
from .cache import Cache
from .error import HTTPError, InvalidArgument
from .queries import ENTRY_ID, ENTRY_ID_CHARACTERS, ENTRY_ID_REVIEWS, ENTRY_TITLE
from .models.character import Character
from .models.enums import Fetchable

if TYPE_CHECKING:
    from .models.anime import Anime
    from .models.core import Review
    from .models.manga import Manga

__all__ = ("HTTPClient",)
__log__ = logging.getLogger(__name__)

class HTTPClient:
    def __init__(
        self,
        session: aiohttp.ClientSession,
        cache_expiration: int,
        entries: dict,
        token: str = None,
    ) -> None:
        self.__authorization = f"Bearer {token}" if token else ""
        self.__session = session
        self.__headers = {
            "Accept": "application/vnd.api+json",
            "Content-Type": "application/vnd.api+json",
            "User-Agent": f"askitsu (https://github.com/ShomyKohai/askitsu {__version__})",
            "Authorization": self.__authorization,
        }
        self._entries = entries
        self._cache: Cache = Cache(expiration=cache_expiration)
        self._cache_expiration = cache_expiration
        self.token: Optional[str] = token

    @property
    def session(self) -> aiohttp.ClientSession:
        return self.__session

    async def post_data(self, data: dict) -> Any:
        async with self.__session.post(
            url="https://kitsu.io/api/graphql", json=data, headers=self.__headers
        ) as response:
            if response.status == 200:
                __log__.info(
                    "Sent a request to Kitsu API"
                )
                return await response.json()
            else:
                raise HTTPError("Something went wrong.", response.status)

    async def _search_entry(
        self, entry_type: Fetchable, query: str, limit: int, method: str
    ):
        cache_res = await self._cache.get(
            f"{entry_type.value}_{query.replace(' ', '_')}_{limit}"
        )
        if cache_res:
            return cache_res.value if len(cache_res.value) > 1 else cache_res.value[0]
        try:
            entry = self._entries[entry_type.value]
        except (KeyError, TypeError):
            raise InvalidArgument
        variables = {"title": query, "limit": limit}
        query_fetch = ENTRY_TITLE.get(method)
        data = await self.post_data(data={"query": query_fetch, "variables": variables})
        __log__.info(f"Sent request to Kitsu API: {method}")
        if not data["data"][method]:
            return None
        fetched = [
            entry(attributes=attributes, http=self, cache=self._cache)
            for attributes in data["data"][method]["nodes"]
        ]
        await self._cache.add(
            f"{entry_type.value}_{query.replace(' ', '_')}_{limit}",
            fetched,
            remove_after=self._cache_expiration,
        )
        __log__.debug(f"Added {entry_type.value}_{query.replace(' ', '_')}_{limit} to cache")
        return fetched if len(fetched) > 1 else fetched[0]

    async def _get_entry_fetch(self, entry_type: Fetchable, id: int, method: str):
        cache_res = await self._cache.get(f"{entry_type.value}_{id}")
        if cache_res:
            return cache_res.value
        try:
            entry = self._entries[entry_type.value]
        except (KeyError, TypeError):
            raise InvalidArgument
        variables = {"id": id}
        query_fetch = ENTRY_ID.get(method)
        data = await self.post_data(data={"query": query_fetch, "variables": variables})
        if not data["data"][method]:
            return None
        fetched_entry = entry(
            attributes=data["data"][method], http=self, cache=self._cache
        )
        await self._cache.add(f"{entry_type.value}_{id}", fetched_entry)
        __log__.debug(f"Added {entry_type.value}_{id} to cache")
        return fetched_entry

    async def _get_reviews_fetch(
        self, entry: Union[Manga, Anime], method: str, limit: int = 1
    ) -> Optional[List[Review]]:
        variables = {"id": entry.id, "limit": limit}
        query_fetch = ENTRY_ID_REVIEWS.get(method)
        data = await self.post_data(data={"query": query_fetch, "variables": variables})
        if not data["data"][method]:
            return None
        return [
            Review(entry.id, entry.entry_type, attributes)
            for attributes in data["data"][method]["reactions"]["nodes"]
        ]

    async def _get_characters_fetch(
        self, entry: Union[Manga, Anime], method: str
    ) -> Optional[List[Character]]:
        cache_res = await self._cache.get(f"{entry.entry_type}_characters")
        if cache_res:
            return cache_res.value
        variables = {"id": entry.id, "limit": 100}
        query_fetch = ENTRY_ID_CHARACTERS.get(method)
        data = await self.post_data(data={"query": query_fetch, "variables": variables})
        if not data["data"][method]:
            return None
        character = [
            Character(attributes, entry_id=entry.id)
            for attributes in data["data"][method]["characters"]["nodes"]
        ]
        await self._cache.add(f"{entry.entry_type}_characters", character)
        return character

    async def close(self) -> None:
        return await self.__session.close()
