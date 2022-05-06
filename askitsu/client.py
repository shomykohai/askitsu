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

import aiohttp
from typing import (
    Any, 
    Optional, 
    Union, 
    List,
    Literal
)
from .anime import Anime, StreamLink
from .character import Character
from .manga import Manga
from .error import *


BASE: str = "https://kitsu.io/api/edge/"


class Client:
    """Represents a client connection to get data from Kitsu.io API

    Parameters
    -----------
    session: Optional[:class:`aiohttp.ClientSession`]
        An object that represents the effective connection

    """

    def __init__(self, session: Optional[aiohttp.ClientSession] = None):
        self._entries = {
            "anime": Anime,
            "manga": Manga,
        }
        self._session: aiohttp.ClientSession = session or aiohttp.ClientSession()
        self._headers = {
            "Accept": "application/vnd.api+json",
            "Content-Type": "application/vnd.api+json",
        }

    async def _get_data(self, url: str) -> Any:
        async with self._session.get(url=url, headers=self._headers) as response:
            response_data = await response.json()
            if response.status == 200:
                return response_data
            if response.status == 404:
                return

    async def search(
        self, type: Literal["anime", "manga"], query: str, limit: int = 1
    ) -> Optional[Union[Anime, List[Anime], Manga, List[Manga]]]:
        """|coro|

        Search trough Kitsu API with the providen query and fetch the found data

        Parameters
        -----------
        type: :class:`str`
            The type of media to search
        query: :class:`str`
            Represents the search query
        limit: :class:`int`
            Limit the search to a specific number of results

        """
        entry = self._entries.get(type)
        fetched_data = await self._get_data(
            f"{BASE}/{type}?filter%5Btext%5D={query}&page%5Blimit%5D={limit}"
        )
        if not fetched_data["data"]:
            return None
        if len(fetched_data["data"]) == 1:
            return entry(type, fetched_data["data"][0])
        return [
            entry(type=type, attributes=attributes)
            for attributes in fetched_data["data"]
        ]

    async def search_anime(
        self, query: str, limit: int = 1
    ) -> Optional[Union[Anime, List[Anime]]]:
        """|coro|

        Shortcut function to :coro:`search` with the `type` parameter populated by the "anime" keyword

        Parameters
        -----------
        query: :class:`str`
            Represents the search query
        limit: :class:`int`
            Limit the search to a specific number of results
        """
        return await self.search("anime", query=query, limit=limit)

    async def search_manga(
        self, query: str, limit: int = 1
    ) -> Optional[Union[Manga, List[Manga]]]:
        """|coro|

        Shortcut function to :coro:`search` with the `type` parameter populated by the "manga" keyword

        Parameters
        -----------
        query: :class:`str`
            Represents the search query
        limit: :class:`int`
            Limit the search to a specific number of results
        """
        return await self.search("manga", query=query, limit=limit)

    async def get_entry(self, type: str, id: int) -> Union[Anime, Manga]:
        """|coro|

        Get an entry object (`Anime` | `Manga`) by an id

        Parameters
        -----------
        type: :class:`str`
            The type of media to fetch
        id: :class:`int`
            ID of the media
        """
        entry = self._entries.get(type)
        fetched_data = await self._get_data(f"{BASE}/{type}/{id}")
        return entry(type, fetched_data["data"])

    async def get_anime_entry(self, id: int) -> Anime:
        """|coro|

        Shortcut for :coro:`get_entry`; returns only `Anime` object

        Parameters
        -----------
        id: :class:`int`
            ID of the anime
        """
        return await self.get_entry("anime", id=id)

    async def get_stream_links(self, anime: Anime) -> List[StreamLink]:
        """|coro|

        Return all streaming link of an Anime object

        Parameters
        -----------
        anime: :class:`Anime`
            The anime to get stream links
        """
        if not isinstance(anime, Anime):
            return InvalidArgument
        fetched_data = await self._get_data(
            url=f"{BASE}/anime/{anime.id}/streaming-links"
        )
        stream_links = []
        for links in fetched_data["data"]:
            stream_links.append(StreamLink(links))
        return stream_links

    async def get_characters(
        self, entry: Union[Anime, Manga], limit: int = 1
    ) -> Union[Character, List[Character]]:
        """|coro|

        Return a :class:`Character` | List[:class:`Character`] 

        Parameters
        -----------
        entry: Union[:class:`Anime`, :class:`Manga`]
            A valid entry to get characters
        limit: :class:`int`
            Number of characters' fetch
        """
        fetched_data = await self._get_data(
            url=f"{BASE}/{entry.type}/{entry.id}/characters?page%5Blimit%5D={limit}"
        )
        characters_roles = [
            link["attributes"]["role"]
            for link in fetched_data["data"]
        ]
        characters_link = [
            link["relationships"]["character"]["links"]["related"]
            for link in fetched_data["data"]
        ]
        characters = [await Character._character_instance(
            links, 
            self, 
            entry.id, 
            role) 
            for links, role in zip(characters_link, characters_roles)
        ]
        return characters if len(characters)>1 else characters[0]

    async def close(self) -> None:
        """
        Close client connection
        """
        return await self._session.close()
