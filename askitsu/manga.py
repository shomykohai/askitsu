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

__all__ = ("Manga", "Chapter")

from datetime import datetime
from typing import Union, List, Optional

from .core import Entry
from .http import HTTPClient


class Chapter:
    """
    Represent a :class:`Manga` chapter


    Attributes
    -----------
    id: :class:`int`
        ID of the chapter
    synopsis: :class:`str`
        Synopsis of the chapter
    description: :class:`str`
        Full description of the chapter
    title: :class:`str`
        Title of the chapter
    volume_number: :class:`int`
        Which volume the chapter belong to
    chapter: :class:`int`
        Chapter number
    lenght: :class:`int`
        Pages of the chapter
    thumbnail: :class:`str`
        Url of the thumbnail
    """

    __slots__ = (
        "id",
        "synopsis",
        "description",
        "title",
        "volume_number",
        "chapter",
        "length",
        "thumbnail",
        "_attributes",
    )

    def __init__(self, attributes: dict) -> None:
        data = attributes["attributes"]
        self._attributes = attributes
        self.id: int = int(attributes["id"])
        self.synopsis: str = data["synopsis"]
        self.description: str = data["description"]
        self.title: str = data["canonicalTitle"]
        self.volume_number: int = data["volumeNumber"]
        self.chapter: int = data["number"]
        self.length: int = data["length"]
        self.thumbnail: str = (
            data["thumbnail"]["original"] if data["thumbnail"] else None
        )

    @property
    def created_at(self) -> Optional[datetime]:
        """Date when a chapter got added on Kitsu DB"""
        try:
            return datetime.strptime(
                self._attributes["createdAt"], "%Y-%m-%dT%H:%M:%S.%fZ"
            )
        except ValueError:
            return None

    @property
    def updated_at(self) -> Optional[datetime]:
        try:
            return datetime.strptime(
                self._attributes["updatedAt"], "%Y-%m-%dT%H:%M:%S.%fZ"
            )
        except ValueError:
            return None

    @property
    def published(self) -> Optional[datetime]:
        """Date when a Chapter got published (YYYY-mm-dd)"""
        try:
            return datetime.strptime(self._attributes["published"], "%Y-%m-%d")
        except ValueError:
            return None


class Manga(Entry):
    """Represents a :class:`Manga` instance

    Attributes
    -----------
    id: :class:`int`
        ID of the manga
    status: :class:`str`
        Actual status of the given manga (E.g. "finished")
    slug: :class:`str`
        String identifier. Work as id to fetch data
    synopsis: :class:`str`
        Description of the given manga
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
    serialization: :class:`str`
        Return manga serialization
    rating_rank: :class:`int`
        Return rating rank
    popularity_rank: :class:`int`
        Return popularity rank position
    rating: :class:`float`
        The rating received from the community in a scale from 1 to 100

        .. versionadded:: 0.4.0

    age_rating: Literal['G', 'PG', 'R', 'R18']
        Age rating of the manga

        .. versionadded:: 0.4.0

    subtype: Literal['doujin', 'manga', 'manhua', 'manhwa', 'novel', 'oel', 'oneshot']
        The subtype of the manga

        .. versionadded:: 0.4.1
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
    )

    def __init__(self, attributes: dict, http: HTTPClient, *args) -> None:
        data = attributes["attributes"]
        self._http = http
        self.entry_type: str = "manga"
        self.chapter_count: int = data["chapterCount"]
        self.volume_count: int = data["volumeCount"]
        self.serialization: str = data["serialization"]
        super().__init__(attributes["id"], self.entry_type, data, http, *args)

    def __repr__(self) -> str:
        return f"<Manga name='{self.canonical_title}' id={self.id}>"

    async def chapters(self, limit: int = 12) -> Union[Chapter, List[Chapter]]:
        """
        Returns a chapter list of chapters

        .. versionadded:: 0.4.0

        limit: :class:`int`
            Limit of chapters to fetch. Defaults to 12 (Max 20).
        """
        data = await self._http.get_data(
            url=f"manga/{self.id}/chapters?page[limit]={limit}"
        )
        chapters = [Chapter(attributes) for attributes in data["data"]]
        return chapters if len(chapters) > 1 else chapters[0]
