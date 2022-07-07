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

from datetime import datetime
from typing import List, Literal, Optional, Union

from .character import Character
from .http import HTTPClient
from .images import CoverImage, PosterImage


__all__ = ("Category", "Review", "Title", "Object")


class Entry:

    __slots__ = (
        "id",
        "entry_type",
        "status",
        "slug",
        "synopsis",
        "canonical_title",
        "rating_rank",
        "popularity_rank",
        "rating",
        "age_rating",
        "subtype",
        "_titles",
        "_attributes",
        "_http",
    )

    def __init__(self, _id: int, _type: str, attributes: dict, http: HTTPClient):
        self._http = http
        self._attributes = attributes
        self._titles: dict = attributes["titles"]
        self.id = int(_id)
        self.entry_type = _type
        self.status: str = attributes["status"]
        self.slug: str = attributes["slug"]
        self.synopsis: str = attributes["synopsis"]
        self.canonical_title: str = attributes["canonicalTitle"]
        self.rating_rank = attributes["ratingRank"]
        self.popularity_rank = attributes["popularityRank"]
        self.rating: float = attributes["averageRating"]
        self.age_rating: Literal["G", "PG", "R", "R18"] = attributes["ageRating"]
        self.subtype: str = attributes["subtype"]

    @property
    def created_at(self) -> Optional[datetime]:
        """When the media got added in Kitsu database"""
        try:
            return datetime.strptime(
                self._attributes["createdAt"], "%Y-%m-%dT%H:%M:%S.%fZ"
            )
        except ValueError:
            return None

    @property
    def updated_at(self) -> Optional[datetime]:
        """Last time the media got updated in Kitsu database"""
        try:
            return datetime.strptime(
                self._attributes["updatedAt"], "%Y-%m-%dT%H:%M:%S.%fZ"
            )
        except ValueError:
            return None

    @property
    def started_at(self) -> Optional[datetime]:
        """Date when the Media started"""
        try:
            return datetime.strptime(self._attributes["startDate"], "%Y-%m-%d")
        except ValueError:
            return None

    @property
    def ended_at(self) -> Optional[datetime]:
        """Date when Media ended"""
        try:
            return datetime.strptime(self._attributes["endDate"], "%Y-%m-%d")
        except ValueError:
            return None

    @property
    def url(self) -> str:
        """
        url: :class:`str`
        Returns url to Kitsu.io website

        .. versionadded:: 0.4.0
        """
        return f"https://kitsu.io/{self.entry_type}/{self.slug}"

    @property
    def title(self) -> Title:
        """
        Return canon title of the given Media

        .. versionchanged:: 0.4.1

        Now it returns an instance of :class:`askitsu.Title`
        """
        return Title(self._titles, self.id, self.entry_type)

    @property
    def poster_image(self) -> PosterImage:
        """
        Return poster image dict with all sizes

        .. versionchanged:: 0.4.1

        Now it returns a poster image object
        """
        return PosterImage(self._attributes["posterImage"], self.id, self.entry_type)

    @property
    def cover_image(self) -> CoverImage:
        """
        Return cover image dict with all sizes

        .. versionchanged:: 0.4.1

        Now it returns a cover image object
        """
        return CoverImage(self._attributes["coverImage"], self.id, self.entry_type)

    @property
    async def categories(self) -> List[Category]:
        """
        Categories of the Media

        .. versionadded:: 0.4.0
        """
        data = await self._http.get_data(url=f"{self.entry_type}/{self.id}/categories")
        return [Category(attributes) for attributes in data["data"]]

    @property
    async def characters(self) -> Union[Character, List[Character]]:
        """
        Get all characters (Max 20)

        .. versionadded:: 0.4.1

        Note
        --------------
        Use :meth:`askitsu.Client.get_characters` if you want to set a limit\n
        The limit with this property is automatically set to 20 (The highest)
        """
        data = await self._http.get_data(
            url=f"{self.entry_type}/{self.id}/characters?include=character&page%5Blimit%5D=20"
        )
        characters_roles = [link["attributes"]["role"] for link in data["data"]]
        characters = [
            Character(attributes, role=role, entry_id=self.id)
            for attributes, role in zip(data["included"], characters_roles)
        ]
        return characters if len(characters) > 1 else characters[0]

    async def reviews(self, limit: int = 1) -> Optional[Union[Review, List[Review]]]:
        """
        Get all the reviews of the Media

        .. versionadded:: 0.3.0
        """
        data = await self._http.get_data(
            url=f"{self.entry_type}/{self.id}/reviews?page%5Blimit%5D={limit}"
        )
        reviews = [
            Review(self.id, self.entry_type, reviews) for reviews in data["data"]
        ]
        return (reviews if limit > 1 else reviews[0]) if reviews else None


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

    __slots__ = ("title", "description", "slug", "nsfw", "_attributes")

    def __init__(self, attributes: dict) -> None:
        self._attributes = attributes["attributes"]
        self.title: str = self._attributes["title"]
        self.description: str = self._attributes["description"]
        self.slug: str = self._attributes["slug"]
        self.nsfw: bool = self._attributes["nsfw"]

    def __repr__(self) -> str:
        return f"<Category title={self.title}>"

    @property
    def created_at(self) -> Optional[datetime]:
        """When a category got added in Kitu DB"""
        try:
            return datetime.strptime(
                self._attributes["createdAt"], "%Y-%m-%dT%H:%M:%S.%fZ"
            )
        except ValueError:
            return None

    @property
    def updated_at(self) -> Optional[datetime]:
        """Last time a category got updated"""
        try:
            return datetime.strptime(
                self._attributes["updatedAt"], "%Y-%m-%dT%H:%M:%S.%fZ"
            )
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
    content_formatted: :class:`str`
        Formatted content of the review
    likes_count: :class:`int`
        How many likes a reviews has
    progress: :class:`str`
    rating: :class:`int`
        Rating of the review
    source: :class:`int`
        Source of the review
    spoiler: :class:`bool`
        If the review is/has a spoiler or not
    """

    __slots__ = (
        "id",
        "content",
        "content_formatted",
        "likes_count",
        "progress",
        "rating",
        "source",
        "spoiler",
        "media_id",
        "media_type",
    )

    def __init__(self, entry_id: int, entry_type: str, attributes: dict) -> None:
        data = attributes["attributes"]
        self.media_id = entry_id
        self.media_type = entry_type
        self.id: str = attributes["id"]
        self.content: str = data["content"]
        self.content_formatted: str = data["contentFormatted"]
        self.likes_count: int = data["likesCount"]
        self.progress: str = data["progress"]
        self.rating: int = data["rating"]
        self.source: str = data["source"]
        self.spoiler: bool = data["spoiler"]


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

    def __init__(
        self, data: dict, entry_id: int = None, entry_type: str = None
    ) -> None:
        self.__data = data
        self.entry_id = entry_id
        self.entry_type = entry_type

    @property
    def en(self) -> Optional[str]:
        return self.__data.get("en")

    @property
    def en_jp(self) -> Optional[str]:
        return self.__data.get("en_jp")

    @property
    def romaji(self) -> Optional[str]:
        return self.en_jp

    @property
    def ja_jp(self) -> Optional[str]:
        return self.__data.get("ja_jp")


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
