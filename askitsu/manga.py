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

__all__ = ('Manga', 'Chapter')

import aiohttp
from datetime import datetime
from typing import Union, List
from .core import Entry, BASE

class Chapter:
    """
    Represent a :class:`Manga` chapter


    Attributes
    -----------
    id: :class:`int`
        ID of the chapter
    created_at: :class:`datetime`
    updated_at: :class:`datetime`
    published: :class:`datetime`
        When the chapter got published (YYYY-mm-dd)
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
    __slots__ = ('id', 'created_at', 'updated_at', 'synopsis', 'description',
                'published', 'title', 'volume_number', 'chapter', 'length', 
                'thumbnail')

    def __init__(self, attributes: dict) -> None:
        data = attributes['attributes']
        self.id: int = attributes['id']
        self.created_at: datetime = datetime.strptime(data['createdAt'], "%Y-%m-%dT%H:%M:%S.%fZ") if (
            data['createdAt']) else None
        self.updated_at: datetime = datetime.strptime(data['updatedAt'], "%Y-%m-%dT%H:%M:%S.%fZ") if (
            data['updatedAt']) else None
        self.published: datetime = datetime.strptime(data['published'], "%Y-%m-%d") if (
            data['published']) else None
        self.synopsis: str = data['synopsis']
        self.description: str = data['description']
        self.title: str = data['canonicalTitle']
        self.volume_number: int = data['volumeNumber']
        self.chapter: int = data['number']
        self.length: int = data['length']
        self.thumbnail: str = data['thumbnail']['original'] if data['thumbnail'] else None

class Manga(Entry):
    """Represents a :class:`Manga` instance 

    Attributes
    -----------
    id: :class:`int`
        ID of the manga
    status: :class:`str`
        Actual status of the given manga (Ex. "finished")
    created_at: Optional[:class:`datetime`]
    updated_at: Optional[:class:`datetime`]
    started_at: Optional[:class:`datetime`]
    ended_at: Optional[:class:`datetime`]
    slug: :class:`str`
        String identifier. Work as id to fetch data
    synopsis: :class:`str`
        Description of the given manga
    title: :class:`str`
        Return canon title of the given manga
    chapter_count: :class:`int`
        Number of chapters
    volume_count: :class:`int`
        Number of volumes
    serialization: :class:`str`
        Return manga serialization
    cover_image: :class:`str`
        Return cover image
    poster_image: :class:`str`
        Return poster image
    rating_rank: :class:`int`
        Return rating rank
    popularity_rank: :class:`int`
        Return popularity rank position
    url: :class:`str`
        Returns url to Kitsu.io website
    rating: :class:`float`
        The rating received from the community in a scale from 1 to 100
    age_rating: Literal['G', 'PG', 'R', 'R18']
        Age rating of the manga
    categories: List[:class:`Category`]
        Categories of the manga
    """

    __slots__ = ('id', 'entry_type', 'status', 'created_at', 'updated_at', 'started_at', 'ended_at',
                'slug', 'synopsis', 'title', 'cover_image', 'poster_image', 'rating_rank',
                'popularity_rank', 'chapter_count', 'volume_count', 'serialization', 'rating', 
                'age_rating','_session')

    def __init__(self, attributes: dict, session: aiohttp.ClientSession, *args) -> None:
        data = attributes['attributes']
        self._session = session
        self.entry_type: str = "manga"
        self.chapter_count: int = data['chapterCount']
        self.volume_count: int = data['volumeCount']
        self.serialization: str = data['serialization']
        super().__init__(attributes['id'], self.entry_type, data, session, *args)


    async def chapters(self, limit: int = 12) -> Union[Chapter, List[Chapter]]:
        async with self._session.get(
            url=f"{BASE}/manga/{self.id}/chapters?page[limit]={limit}"
        ) as data:
            fetched_data = await data.json()
            chapters = [Chapter(attributes) for attributes in fetched_data["data"]]
            return chapters if len(chapters)>1 else chapters[0]