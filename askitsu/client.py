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
from colorama import Fore, Style  # type: ignore
from typing import Dict, List, Literal, Optional, overload, Type, Union


from .queries import (
    QUERY_METHODS,
    TRENDING_ENTRY,
    USERS_BY_ID,
    USER_BY_USERNAME,
)
from .error import InvalidArgument
from .http import HTTPClient
from .models.anime import Anime
from .models.character import Character
from .models.core import Review
from .models.enums import Entries, Media, Fetchable
from .models.manga import Manga
from .models.users import User


__all__ = ("Client",)


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

    def __init__(
        self,
        token: str = None,
        *,
        session: Optional[aiohttp.ClientSession] = None,
        cache_expiration: int = 300,
    ) -> None:
        self._entries: Dict[str, Union[Type[Anime], Type[Manga], Type[Character]]] = {
            "anime": Anime,
            "manga": Manga,
            "characters": Character,
        }
        self.http: HTTPClient = HTTPClient(
            session=session or aiohttp.ClientSession(),
            cache_expiration=cache_expiration,
            token=token,
            entries=self._entries,
        )

    @property
    def session(self) -> aiohttp.ClientSession:
        return self.http.session

    @property
    def token(self) -> Optional[str]:
        return self.http.token

    @overload
    async def search(self, type: Literal[Entries.ANIME], query: str) -> Optional[Anime]:
        ...

    @overload
    async def search(
        self, type: Literal[Entries.ANIME], query: str, limit: int
    ) -> Optional[List[Anime]]:
        ...

    @overload
    async def search(self, type: Literal[Entries.MANGA], query: str) -> Optional[Manga]:
        ...

    @overload
    async def search(
        self, type: Literal[Entries.MANGA], query: str, limit: int
    ) -> Optional[List[Manga]]:
        ...

    @overload
    async def search(
        self, type: Literal[Entries.CHARACTER], query: str
    ) -> Optional[Character]:
        ...

    @overload
    async def search(
        self, type: Literal[Entries.CHARACTER], query: str, limit: int
    ) -> Optional[List[Character]]:
        ...

    async def search(
        self, type: Fetchable, query: str, limit: int = 1
    ) -> Optional[
        Union[Anime, List[Anime], Manga, List[Manga], Character, List[Character]]
    ]:
        """|coro|

        Search trough Kitsu API with the providen query and fetch the found data

        Parameters
        -----------
        type: :class:`Entries`
            The type of entry to search
        query: :class:`str`
            Represents the search query
        limit: :class:`int`
            Limit the search to a specific number of results

        """
        try:
            method = QUERY_METHODS[f"{type.value}_search"]
        except (KeyError, TypeError):
            raise InvalidArgument
        else:
            return await self.http._search_entry(
                entry_type=type, query=query, limit=limit, method=method
            )

    @overload
    async def search_anime(self, query: str) -> Optional[Anime]:
        ...

    @overload
    async def search_anime(self, query: str, limit: int) -> Optional[List[Anime]]:
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
        return await self.search(Entries.ANIME, query=query, limit=limit)

    @overload
    async def search_manga(self, query: str) -> Optional[Manga]:
        ...

    @overload
    async def search_manga(self, query: str, limit: int) -> Optional[List[Manga]]:
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
        return await self.search(Entries.MANGA, query=query, limit=limit)

    #############################
    #    SEARCH CHARACTERS ?    #
    #############################

    async def search_user(self, name: str) -> Optional[User]:
        """
        Fetch a user by their username

        name: :class:`str`
            Nickname of the user to fetch
        """
        cache_res = await self.http._cache.get(f"user_{name}")
        if cache_res:
            return cache_res.value
        variables = {"name": name}
        data = await self.http.post_data(
            data={"query": USER_BY_USERNAME, "variables": variables}
        )
        user = User(
            data["data"]["searchProfileByUsername"]["nodes"][0],
            http=self.http,
            cache=self.http._cache,
        )
        await self.http._cache.add(
            f"user_{name}", user, remove_after=self.http._cache_expiration
        )
        return user

    @overload
    async def get_entry(self, type: Literal[Entries.ANIME], id: int) -> Anime:
        ...

    @overload
    async def get_entry(self, type: Literal[Entries.MANGA], id: int) -> Manga:
        ...

    @overload
    async def get_entry(self, type: Literal[Entries.CHARACTER], id: int) -> Character:
        ...

    async def get_entry(
        self, type: Fetchable, id: int
    ) -> Optional[Union[Anime, Manga, Character]]:
        """|coro|

        Get an entry object (`Anime` | `Manga` | `Character`) by an id

        Parameters
        -----------
        type: :class:`Entries`
            The type of media to fetch
        id: :class:`int`
            ID of the media
        """
        try:
            method = QUERY_METHODS[f"{type.value}_id"]
        except (KeyError, TypeError):
            raise InvalidArgument
        else:
            return await self.http._get_entry_fetch(
                entry_type=type, id=id, method=method
            )

    async def get_anime_entry(self, id: int) -> Anime:
        """|coro|

        Shortcut for :meth:`get_entry`; returns only `Anime` object

        Parameters
        -----------
        id: :class:`int`
            ID of the anime
        """
        return await self.get_entry(Entries.ANIME, id=id)

    async def get_manga_entry(self, id: int) -> Manga:
        """|coro|

        Shortcut for :meth:`get_entry`; returns only `Manga` object

        .. versionadded:: 0.3.0

        Parameters
        -----------
        id: :class:`int`
            ID of the manga
        """
        return await self.get_entry(Entries.MANGA, id=id)

    @overload
    async def get_trending_entry(
        self, type: Literal[Entries.ANIME], limit: int = ...
    ) -> List[Anime]:
        ...

    @overload
    async def get_trending_entry(
        self, type: Literal[Entries.MANGA], limit: int = ...
    ) -> List[Manga]:
        ...

    async def get_trending_entry(
        self, type: Media, limit: int = 10
    ) -> Optional[Union[List[Anime], List[Manga]]]:
        """|coro|

        Return a list of anime or manga (max of 10)

        .. versionadded:: 0.2.1

        Parameters
        -----------
        entry: Union[:class:`Anime`, :class:`Manga`]
            Entry to fetch its trending
        """
        type_upper = type.value.upper()
        if type_upper not in ("ANIME", "MANGA"):
            raise InvalidArgument(
                f"{Fore.RED}{type_upper.capitalize} cannot be fetched in trending list\n"
                f"Please pass 'anime' or 'manga' as parameter to {Fore.LIGHTCYAN_EX}get_trending_entry{Style.RESET_ALL}"
            )
        try:
            entry = self._entries[type_upper.lower()]
        except (KeyError, TypeError):
            raise InvalidArgument
        variables = {"media": type_upper, "limit": limit}
        data = await self.http.post_data(
            data={"query": TRENDING_ENTRY, "variables": variables}
        )
        data_value = data["data"]["globalTrending"]["nodes"]
        return (
            [
                entry(attributes=attributes, http=self.http, cache=self._cache)
                for attributes in data_value
            ]
            if data_value
            else None  # type: ignore
        )

    async def get_reviews(
        self, entry: Union[Anime, Manga], limit: int = 1
    ) -> Optional[List[Review]]:
        """|coro|

        Get reviews of a given entry

        .. versionadded:: 0.3.0

        Parameters
        -----------
        entry: Union[:class:`Anime`, :class:`Manga`]
            A valid entry to get reviews (Can also be :class:`Object`)
        limit: :class:`int`
            Limit to reviews to fetch
        """
        type_lower = entry.entry_type.lower()
        try:
            method = QUERY_METHODS[f"{type_lower}_id"]
        except (KeyError, TypeError):
            raise InvalidArgument
        else:
            return await self.http._get_reviews_fetch(
                entry=entry, method=method, limit=limit
            )

    async def get_characters(
        self, entry: Union[Anime, Manga]
    ) -> Optional[List[Character]]:
        """|coro|

        Return a :class:`Character` | List[:class:`Character`]

        Parameters
        -----------
        entry: Union[:class:`Anime`, :class:`Manga`]
            A valid entry to get characters (Can also be :class:`Object`)
        limit: :class:`int`
            Number of characters to fetch
        """
        type_lower = entry.entry_type.lower()
        try:
            method = QUERY_METHODS[f"{type_lower}_id"]
        except (KeyError, TypeError):
            raise InvalidArgument
        else:
            return await self.http._get_characters_fetch(entry=entry, method=method)

    async def get_user(self, id: int) -> Optional[User]:
        """|coro|

        Get a user by their id

        .. versionadded:: 0.5.0

        Parameters
        -----------
        id: :class:`int`
            The id of the user to fetch
        """
        cache_res = await self.http._cache.get(f"user_{id}")
        if cache_res:
            if cache_res.value is not None:
                return cache_res.value
            await self.http._cache.remove(f"user_{id}")
        variables = {"id": id}
        data = await self.http.post_data(
            data={"query": USERS_BY_ID, "variables": variables}
        )
        user = (
            User(
                data["data"]["findProfileById"], http=self.http, cache=self.http._cache
            )
            if data["data"]
            else None
        )
        await self.http._cache.add(f"user_{id}", user)
        return user

    async def check_user(self, slug: str) -> bool:
        """|coro|

        Check if the user exists on Kitsu

        .. versionadded:: 0.5.0

        Parameters
        -----------
        slug: :class:`str`
            Nickname of the user
        """
        query = """
            query checkUser ($slug: String!) {
                findProfileBySlug(slug: $slug) {
                    slug
                }
            }
        """
        cache_res = await self.http._cache.get(f"user_{slug}")
        if cache_res:
            return True
        variables = {"slug": slug}
        data = await self.http.post_data(data={"query": query, "variables": variables})
        if data["data"]["findProfileBySlug"] is not None:
            await self.http._cache.add(f"user_{slug}", None)
        return bool(data["data"]["findProfileBySlug"])

    async def close(self) -> None:
        """Close client connection"""
        return await self.http.close()
