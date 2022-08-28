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

from datetime import datetime
from typing import List, Optional

from .character import Character
from .core import Category, Entry, Review
from ..cache import Cache
from ..http import HTTPClient
from ..queries import (
    BASE_URL,
    MANGA_BY_ID_CATEGORIES,
    MANGA_BY_ID_CHAPTERS,
    MANGA_BY_ID_CHARACTERS,
    MANGA_BY_ID_REVIEWS,
)

__all__ = ("Manga", "Chapter")


class Chapter:
    """
    Represent a :class:`Manga` chapter


    Attributes
    -----------
    id: :class:`int`
        ID of the chapter
    description: :class:`str`
        Full description of the chapter
    title: :class:`str`
        Title of the chapter
    volume_number: :class:`int`
        Which volume the chapter belong to
    chapter: :class:`int`
        Chapter number
    """

    __slots__ = (
        "id",
        "synopsis",
        "description",
        "title",
        "volume_number",
        "chapter",
        "length",
        "_attributes",
    )

    def __init__(self, attributes: dict) -> None:
        self._attributes = attributes
        self.id: int = int(attributes["id"])
        self.description: str = attributes["description"]["en"]
        self.title: str = attributes["titles"]["romanized"]
        self.chapter: int = attributes["number"]
        # self.length: int = attributes["length"]

    @property
    def thumbnail(self) -> Optional[str]:
        """Url of the thumbnail"""
        try:
            return self._attributes["thumbnail"]["original"]["url"]
        except (KeyError, TypeError):
            return None

    # @property
    # def published(self) -> Optional[datetime]:
    #     """Date when a Chapter got published (YYYY-mm-dd)"""
    #     try:
    #         return datetime.strptime(self._attributes["published"], "%Y-%m-%d")
    #     except ValueError:
    #         return None


class Manga(Entry):
    """Represents a :class:`Manga` instance

    Attributes
    -----------
    id: :class:`int`
        ID of the manga
    status: :class:`str`
        Actual status of the given manga (Ex. "finished")
    started_at: Optional[:class:`datetime`]
        Date when the manga started
    ended_at: Optional[:class:`datetime`]
        Date when the manga ended
    slug: :class:`str`
        String identifier. Work as id to fetch data
    title: :class:`str`
        Return canon title of the given manga

        .. versionchanged:: 0.4.1

        Now it returns an instance of :class:`askitsu.Title`
    canonical_title: :class:`str`
        Returns canonical title of the given manga

        .. versionadded:: 0.4.1

    chapter_count: :class:`int`
        Number of chapters
    volume_count: :class:`int`
        Number of volumes
    cover_image: :class:`CoverImage`
        Return cover image dict with all sizes

        .. versionchanged:: 0.4.1

        Now it returns a cover image object

    poster_image: :class:`PosterImage`
        Return poster image dict with all sizes

        .. versionchanged:: 0.4.1

        Now it returns a poster image object

    rating_rank: :class:`int`
        Return rating rank
    popularity_rank: :class:`int`
        Return popularity rank position
    url: :class:`str`
        Returns url to Kitsu.io website

        .. versionadded:: 0.4.0

    rating: :class:`float`
        The rating received from the community in a scale from 1 to 100

        .. versionadded:: 0.4.0

    age_rating: Literal['G', 'PG', 'R', 'R18']
        Age rating of the manga

        .. versionadded:: 0.4.0

    categories: List[:class:`Category`]
        Categories of the manga

        .. versionadded:: 0.4.0

    subtype: Literal['doujin', 'manga', 'manhua', 'manhwa', 'novel', 'oel', 'oneshot']
        The subtype of the manga

        .. versionadded:: 0.4.1

    characters: Union[:class:`Character`, List[:class:`Character`]
        Get all characters (Max 20)

        .. versionadded:: 0.4.1

        Note
        --------------
        Use :meth:`askitsu.Client.get_characters` if you want to set a limit\n
        The limit with this property is automatically set to 20 (The highest)
    """

    __slots__ = (
        "id",
        "entry_type",
        "status",
        "slug",
        "synopsis",
        "canonical_title",
        "rating_rank",
        "popularity_rank",
        "chapter_count",
        "volume_count",
        "serialization",
        "rating",
        "age_rating",
        "subtype",
        "_http",
        "_titles",
        "_attributes",
        "_cache",
    )

    def __init__(self, attributes: dict, http: HTTPClient, cache: Cache) -> None:
        self._http = http
        self.entry_type: str = "manga"
        self.chapter_count: int = attributes["chapterCount"]
        self.volume_count: int = attributes["volumeCount"]
        self.subtype: str = attributes["mangasub"]
        # self.serialization: str = data["serialization"]
        super().__init__(
            _id=attributes["id"],
            _type=self.entry_type,
            attributes=attributes,
            http=http,
            cache=cache,
        )

    def __repr__(self) -> str:
        return f"<Manga name='{self.canonical_title}' id={self.id}>"

    async def chapters(self, limit: int = 12) -> List[Chapter]:
        """
        Returns a chapter list of chapters

        .. versionadded:: 0.4.0

        limit: :class:`int`
            Limit of chapters to fetch. Defaults to 12.
        """
        cache_res = await self._cache.get(f"manga_{self.id}_chapters_{limit}")
        if cache_res:
            return cache_res.value
        variables = {"id": self.id, "limit": limit}
        data = await self._http.post_data(
            url=BASE_URL, data={"query": MANGA_BY_ID_CHAPTERS, "variables": variables}
        )
        chapters = [
            Chapter(attributes)
            for attributes in data["data"]["findMangaById"]["chapters"]["nodes"]
        ]
        await self._cache.add(
            f"manga_{self.id}_chapters_{limit}",
            chapters,
            remove_after=self._cache.expiration,
        )
        return chapters

    @property
    async def categories(self) -> List[Category]:
        cache_res = await self._cache.get(f"manga_{self.id}_categories")
        if cache_res:
            return cache_res.value
        variables = {"id": self.id}
        data = await self._http.post_data(
            url=BASE_URL, data={"query": MANGA_BY_ID_CATEGORIES, "variables": variables}
        )
        categories = [
            Category(attributes)
            for attributes in data["data"]["findMangaById"]["categories"]["nodes"]
        ]
        await self._cache.add(
            f"manga_{self.id}_categories",
            categories,
            remove_after=self._cache.expiration,
        )
        return categories

    @property
    async def characters(self) -> List[Character]:
        cache_res = await self._cache.get(f"manga_{self.id}_characters")
        if cache_res:
            return cache_res.value
        variables = {"id": self.id, "limit": 100}
        data = await self._http.post_data(
            url=BASE_URL, data={"query": MANGA_BY_ID_CHARACTERS, "variables": variables}
        )
        characters = [
            Character(attributes, entry_id=self.id)
            for attributes in data["data"]["findMangaById"]["characters"]["nodes"]
        ]
        await self._cache.add(
            f"manga_{self.id}_characters",
            characters,
            remove_after=self._cache.expiration,
        )
        return characters

    async def reviews(self, limit: int = 1) -> List[Review]:
        variables = {"id": self.id, "limit": limit}
        data = await self._http.post_data(
            url=BASE_URL, data={"query": MANGA_BY_ID_REVIEWS, "variables": variables}
        )
        return [
            Review(self.id, self.entry_type, attributes)
            for attributes in data["data"]["findAnimeById"]["reactions"]["nodes"]
        ]
