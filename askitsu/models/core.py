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

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Literal, Optional


from .character import Character
from .images import CoverImage, PosterImage
from ..cache import Cache
from ..http import HTTPClient

__all__ = ("Category", "Review", "Title", "Object")


class Category:
    """
    Represent a category of a media.

    .. versionadded:: 0.4.0

    Attributes
    ------------
    title: :class:`str`
        Title of the category
    description: :class:`str`
        Description of the category
    slug: :class:`str`
        Identifier string of the category
    nsfw: :class:`bool`
        If the category is NSFW or not
    """

    __slots__ = (
        "title", 
        "description", 
        "slug", 
        "nsfw",
        "_attributes"
    )

    def __init__(self, attributes: dict) -> None:
        self._attributes = attributes
        self.title: str = attributes["title"]["en"]
        self.description: str = attributes["description"]
        self.slug: str = attributes["slug"]
        self.nsfw: bool = attributes["isNsfw"]

    def __repr__(self) -> str:
        return f"<Category title={self.title}>"

    @property
    def created_at(self) -> Optional[datetime]:
        """When a category got added in Kitu DB"""
        try:
            return datetime.strptime(self._attributes["createdAt"], "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            return None

    @property
    def updated_at(self) -> Optional[datetime]:
        """Last time a category got updated"""
        try:
            return datetime.strptime(self._attributes["updatedAt"], "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            return None

class Review:
    """Represents a :class:`Review` instance.
    Reviews belong to a media (:class:`Anime`, :class:`Manga`)

    .. versionadded:: 0.3.0

    Attributes
    -----------
    id: :class:`int`
        ID of the review
    content: :class:`str`
        Content of the review
    progress: :class:`str`
        User's progress of the media at the time
        of the review
    """

    __slots__ = (
        "id",
        "content",
        "progress",
        "media_id",
        "media_type",
    )

    def __init__(self, entry_id: int, entry_type: str, attributes: dict) -> None:
        self.media_id = entry_id
        self.media_type = entry_type
        self.id: str = attributes["id"]
        self.content: str = attributes["reaction"]
        self.progress: str = attributes["progress"]


class Title:
    """
    Represent the various titles that a entry can have

    Attributes
    -----------
    entry_id: :class:`int`
        The id of the media which the title belong to
    entry_type: :class:`str`
        The type of the media (anime, manga)
    en: :class:`str`
        The title of the media in English
    en_jp: :class:`str`
        The title of the media in romanized Japanese
    romaji: :class:`str`
        Same as :attr:`en_jp`
    ja_jp: :class:`str`
        The title of the media in Japanese
    """
    def __init__(self, data: dict, entry_id: int = None, entry_type: str = None) -> None:
        self.__data = data
        self.entry_id = entry_id
        self.entry_type = entry_type

    @property
    def en(self) -> Optional[str]:
        return self.__data.get("en_us")

    @property
    def en_jp(self) -> Optional[str]:
        return self.__data.get("en_jp")

    @property
    def romaji(self) -> Optional[str]:
        return self.en_jp

    @property
    def ja_jp(self) -> Optional[str]:
        return self.__data.get("ja_jp")

class Entry(ABC):

    __slots__ = (
        "id",
        "entry_type",
        "status",
        "slug",
        "description",
        "canonical_title",
        "rating_rank",
        "popularity_rank",
        "rating",
        "age_rating",
        "subtype"
    )

    def __init__(self, _id: int, _type: str, attributes: dict, http: HTTPClient, cache: Cache):
        self._cache: Cache = cache
        self._http: HTTPClient = http
        self._attributes = attributes
        self._titles: dict = attributes["titles"]["localized"]
        self.id = int(_id)
        self.entry_type = _type
        self.status: str = attributes["status"]
        self.slug: str = attributes["slug"]
        self.canonical_title: str = attributes["titles"]["canonical"]
        self.description: str = attributes["description"]["en"]
        self.rating_rank = attributes["averageRatingRank"]
        self.popularity_rank = attributes["userCountRank"]
        self.rating: float = attributes["averageRating"]
        self.age_rating: Literal["G", "PG", "R", "R18"] = attributes["ageRating"]

    @property
    def created_at(self) -> Optional[datetime]:
        try:
            return datetime.strptime(self._attributes["createdAt"], "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            return None

    @property
    def updated_at(self) -> Optional[datetime]:
        try:
            return datetime.strptime(self._attributes["updatedAt"], "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            return None

    @property
    def started_at(self) -> Optional[datetime]:
        try:
            return datetime.strptime(self._attributes["startDate"], "%Y-%m-%d")
        except ValueError:
            return None

    @property
    def ended_at(self) -> Optional[datetime]:
        try:
            return datetime.strptime(self._attributes["endDate"], "%Y-%m-%d")
        except ValueError:
            return None

    @property
    def url(self) -> str:
        return f"https://kitsu.io/{self.entry_type}/{self.slug}"

    @property
    def title(self) -> Title:
        return Title(self._titles, self.id, self.entry_type)
    
    @property
    def poster_image(self) -> PosterImage:
        return PosterImage(
            self._attributes["posterImage"],
            self.id,
            self.entry_type
        )

    @property
    def cover_image(self) -> CoverImage:
        return CoverImage(
            self._attributes["bannerImage"],
            self.id,
            self.entry_type
        )

    @property
    @abstractmethod
    async def categories(self) -> List[Category]:
       ...

    @property
    @abstractmethod
    async def characters(self) -> List[Character]:
        ...

    @abstractmethod
    async def reviews(self, limit: int = 1) -> List[Review]:
        ...


class Object:
    """
    Represent a generic Object.
    This can be useful if you want to use some methods that require a 
    specific istance.
    
    Example:
    If you want to fetch the characters using :meth:`askitsu.Client.get_characters`
    without a :class:`Manga` or :class:`Anime` istance, you can use this class by giving
    an id and an entry_type

    Attributes
    --------------
    id: :class:`int`
        The id of the object
    entry_type: Optional[:class:`str`]
        The type of the object
    """
    def __init__(self, id: int, *, type: str = None) -> None:
        self.id: int = id
        self.entry_type: Optional[str] = type

    def __repr__(self) -> str:
        return f"<Object id={self.id} entry_type={self.entry_type}>"