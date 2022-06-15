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
from colorama import Fore, Style
from typing import (
    Any, 
    List,
    Literal,
    Optional,
    overload,
    Union
)
from .anime import Anime, StreamLink
from .character import Character
from .core import Review, BASE
from .error import (
    BadApiRequest, 
    InvalidArgument,
    NotAuthenticated
)
from . import __version__
from .manga import Manga



class Client:
    """Represents a client connection to get data from Kitsu.io API

    Parameters
    -----------
    token: :class:`str`
        Access token to make authenticated requests.\n
        Useful when you need to fetch NSFW content, interact with users or post something. 

        .. versionadded:: 0.4.1

    session: Optional[:class:`aiohttp.ClientSession`]
        An object that represents the effective connection
    
    Attributes
    -----------
    token: :class:`str`
        Token passed to the session.
    """

    def __init__(self, token: str = None, *, session: Optional[aiohttp.ClientSession] = None) -> None:
        self._entries = {
            "anime": Anime,
            "manga": Manga,
            "characters": Character
        }
        self.__authorization = f"Bearer {token}" if token else ""
        self._session: aiohttp.ClientSession = session or aiohttp.ClientSession()
        self.__headers = {
            "Accept": "application/vnd.api+json",
            "Content-Type": "application/vnd.api+json",
            "User-Agent": f"askitsu (https://github.com/ShomyKohai/askitsu {__version__})",
            "Authorization": self.__authorization
        }
        self.token = token

    async def _get_data(self, url: str) -> Any:
        async with self._session.get(url=url, headers=self.__headers) as response:
            response_data = await response.json()
            if response.status == 200:
                return response_data
            if response.status == 404:
                return None
            if response.status == 401:
                raise NotAuthenticated
            if response.status == 400:
                raise BadApiRequest(response_data["errors"][0])

    @overload
    async def search(
       self, type: Literal["anime"], query: str
    ) -> Optional[Anime]:
        ...
    
    @overload
    async def search(
       self, type: Literal["anime"], query: str, limit: int = ...
    ) -> Optional[List[Anime]]:
        ...

    @overload
    async def search(
       self, type: Literal["manga"], query: str
    ) -> Optional[Manga]:
        ...
    
    @overload
    async def search(
       self, type: Literal["manga"], query: str, limit: int = ...
    ) -> Optional[List[Manga]]:
        ...
    
    @overload
    async def search(
       self, type: Literal["characters"], query: str
    ) -> Optional[Character]:
        ...
    
    @overload
    async def search(
       self, type: Literal["characters"], query: str, limit: int = ...
    ) -> Optional[List[Character]]:
        ...    
       

    async def search(
        self, type: Literal["anime", "manga", "characters"], query: str, limit: int = 1
    ) -> Optional[
        Union[Anime, List[Anime], Manga, List[Manga], Character, List[Character]]
    ]:
        """|coro|

        Search trough Kitsu API with the providen query and fetch the found data

        Parameters
        -----------
        type: Literal["anime", "manga", "characters"]
            The type of entry to search
        query: :class:`str`
            Represents the search query
        limit: :class:`int`
            Limit the search to a specific number of results

        """
        type_lower = type.lower()
        entry = self._entries.get(type_lower)
        filter = "name" if type_lower == "characters" else "text"
        fetched_data = await self._get_data(
            f"{BASE}/{type_lower}?filter%5B{filter}%5D={query}&page%5Blimit%5D={limit}"
        )
        if not fetched_data["data"]:
            return None
        if len(fetched_data["data"]) == 1:
            return entry(fetched_data["data"][0], self._session)
        return [
            entry(attributes=attributes, session=self._session)
            for attributes in fetched_data["data"]
        ]

    @overload
    async def search_anime(
        self, query: str
    ) -> Optional[Anime]:
        ...

    @overload
    async def search_anime(
        self, query: str, limit: int = ...
    ) -> Optional[List[Anime]]:
        ...
   
    async def search_anime(
        self, query: str, limit: int = 1
    ) -> Optional[Union[Anime, List[Anime]]]:
        """|coro|

        Shortcut function to :meth:`search` with the `type` parameter populated by the "anime" keyword

        Parameters
        -----------
        query: :class:`str`
            Represents the search query
        limit: :class:`int`
            Limit the search to a specific number of results
        """
        return await self.search("anime", query=query, limit=limit)

    @overload
    async def search_manga(
        self, query: str
    ) -> Optional[Manga]:
        ...
    @overload
    async def search_manga(
        self, query: str, limit: int = ...
    ) -> Optional[List[Manga]]:
        ...    

    async def search_manga(
        self, query: str, limit: int = 1
    ) -> Optional[Union[Manga, List[Manga]]]:
        """|coro|

        Shortcut function to :meth:`search` with the `type` parameter populated by the "manga" keyword

        Parameters
        -----------
        query: :class:`str`
            Represents the search query
        limit: :class:`int`
            Limit the search to a specific number of results
        """
        return await self.search("manga", query=query, limit=limit)

    @overload
    async def search_character(
        self, query: str
    ) -> Optional[Character]:
        ...

    @overload
    async def search_character(
        self, query: str, limit: int = ...
    ) -> Optional[List[Character]]:
        ...

    async def search_character(
        self, query: str, limit: int = 1
    ) -> Optional[Union[Character, List[Character]]]:
        """|coro|

        Shortcut function to :meth:`search` with the `type` parameter populated by the "character" keyword

        .. versionadded:: 0.3.0

        Parameters
        -----------
        query: :class:`str`
            Represents the search query
        limit: :class:`int`
            Limit the search to a specific number of results

        Note
        ------------
        By searching characters, you will not get :attr:`askitsu.Character.media_id` and :attr:`askitsu.Character.role` attributes
        """
        return await self.search("characters", query=query, limit=limit)


    @overload
    async def get_entry(
        self, type: Literal["anime"], id: int
    ) -> Anime:
        ...

    @overload
    async def get_entry(
        self, type: Literal["manga"], id: int
    ) -> Manga:
        ... 

    @overload
    async def get_entry(
        self, type: Literal["characters"], id: int
    ) -> Character:
        ...

    async def get_entry(
        self, type: Literal["anime", "manga", "characters"], id: int
    ) -> Union[Anime, Manga, Character]:
        """|coro|

        Get an entry object (`Anime` | `Manga` | `Character`) by an id

        Parameters
        -----------
        type: :class:`str`
            The type of media to fetch
        id: :class:`int`
            ID of the media
        """
        type_lower = type.lower()
        entry = self._entries.get(type_lower)
        fetched_data = await self._get_data(f"{BASE}/{type_lower}/{id}")
        return (
            entry(attributes=fetched_data["data"], session=self._session)
            if fetched_data
            else None
        )

    async def get_anime_entry(self, id: int) -> Anime:
        """|coro|

        Shortcut for :meth:`get_entry`; returns only `Anime` object

        Parameters
        -----------
        id: :class:`int`
            ID of the anime
        """
        return await self.get_entry("anime", id=id)

    async def get_manga_entry(self, id: int) -> Manga:
        """|coro|

        Shortcut for :meth:`get_entry`; returns only `Manga` object

        .. versionadded:: 0.3.0

        Parameters
        -----------
        id: :class:`int`
            ID of the manga
        """
        return await self.get_entry("manga", id=id)

    async def get_stream_links(self, anime: Anime) -> List[StreamLink]:
        """|coro|

        Return all streaming link of an Anime object

        Parameters
        -----------
        anime: :class:`Anime`
            The anime to get stream links
        """
        if not isinstance(anime, Anime):
            raise InvalidArgument(
                f"{Fore.RED}'{anime}' is not an istance of Anime\n"
                f"Make sure you pass a valid argument to {Fore.LIGHTCYAN_EX}get_stream_links{Style.RESET_ALL}"
            )
        fetched_data = await self._get_data(
            url=f"{BASE}/anime/{anime.id}/streaming-links"
        )
        return [StreamLink(links) for links in fetched_data["data"]]


    @overload
    async def get_characters(
        self, entry: Union[Anime, Manga]
    ) -> Character:
        ...

    @overload
    async def get_characters(
        self, entry: Union[Anime, Manga], limit: int = ...
    ) -> List[Character]:
        ...

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
            url=f"{BASE}/{entry.entry_type}/{entry.id}/characters?include=character&page%5Blimit%5D={limit}"
        )
        characters_roles = [link["attributes"]["role"] for link in fetched_data["data"]]
        characters = [
            Character(attributes, role=role, entry_id=entry.id) 
            for attributes, role in zip(fetched_data["included"], characters_roles)
        ]
        return characters if len(characters) > 1 else characters[0]

    @overload
    async def get_trending_entry(
        self, type: Literal["anime"]
    ) -> Optional[List[Anime]]:
        ...

    @overload
    async def get_trending_entry(
        self, type: Literal["manga"]
    ) -> Optional[List[Manga]]:
        ...
    
    async def get_trending_entry(
        self, type: Literal["anime", "manga"]
    ) -> Union[List[Anime], List[Manga], None]:
        """|coro|

        Return a list of anime or manga

        .. versionadded:: 0.2.1

        Parameters
        -----------
        entry: Union[:class:`Anime`, :class:`Manga`]
            Entry to fetch its trending
        """
        type_lower = type.lower()
        if type_lower == "characters":
            raise InvalidArgument(
                f"{Fore.RED}Characters can't be fetched in trending list\n"
                f"Please pass 'anime' or 'manga' as parameter to {Fore.LIGHTCYAN_EX}get_trending_entry{Style.RESET_ALL}"
            )
        entry = self._entries.get(type_lower)
        fetched_data = await self._get_data(f"{BASE}/trending/{type_lower}")
        return [
            entry(attributes=attributes, session=self._session)
            for attributes in fetched_data["data"]
        ]


    @overload
    async def get_reviews(
        self, 
        entry: Union[Manga, Anime]
    ) -> Optional[Review]:
        ...

    @overload
    async def get_reviews(
        self, entry: Union[Manga, Anime], limit: int = ...
    ) -> Optional[List[Review]]:
        ...

    async def get_reviews(
        self, entry: Union[Manga, Anime], limit: int = 1
    ) -> Optional[Union[Review, List[Review]]]:
        """|coro|

        Get reviews of a given entry

        .. versionadded:: 0.3.0

        Parameters
        -----------
        entry: Union[Manga, Anime]
            A valid entry to get reviews
        limit: :class:`int`
            Limit to reviews to fetch
        """
        fetched_data = await self._get_data(
            url=f"{BASE}/{entry.entry_type}/{entry.id}/reviews?page%5Blimit%5D={limit}"
        )
        reviews = [
            Review(entry.id, entry.entry_type, reviews)
            for reviews in fetched_data["data"]
        ]
        return (reviews if limit > 1 else reviews[0]) if reviews else None

    async def close(self) -> None:
        """
        Close client connection
        """
        return await self._session.close()
