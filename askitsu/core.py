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

import aiohttp
from datetime import datetime
from typing import Optional, Literal, List

BASE: str = "https://kitsu.io/api/edge/"


class Entry:

    __slots__ = ('id', 'entry_type', 'status', 'created_at', 'updated_at', 'started_at', 'ended_at',
                'slug', 'synopsis', 'title', 'rating_rank', 'popularity_rank', 'rating', 'age_rating')

    def __init__(self, _id: str, _type: str, attributes: dict, session: aiohttp.ClientSession = None):
        self._session = session
        self.id= _id
        self.entry_type = _type
        self.status: str = attributes['status']
        self.created_at: datetime = datetime.strptime(attributes['createdAt'], "%Y-%m-%dT%H:%M:%S.%fZ") if (
            attributes['createdAt']) else None
        self.updated_at: datetime = datetime.strptime(attributes['updatedAt'], "%Y-%m-%dT%H:%M:%S.%fZ") if (
            attributes['updatedAt']) else None
        self.ended_at: datetime = datetime.strptime(attributes['endDate'], "%Y-%m-%d") if (
            attributes['endDate']) else None
        self.slug: str = attributes['slug']
        self.synopsis: str = attributes['synopsis']
        self.title: str = attributes['canonicalTitle']
        self.cover_image = attributes['coverImage']
        self.poster_image = attributes['posterImage']
        self.rating_rank = attributes['ratingRank']
        self.popularity_rank = attributes['popularityRank']
        self.rating: float = attributes['averageRating']
        self.age_rating: Literal['G', 'PG', 'R', 'R18'] = attributes['ageRating']


    def get_cover_image(
        self, 
        _size: Optional[Literal["tiny", "small", "large", "original"]] = "original"
    ) -> Optional[str]:
        """Get the cover image

        Parameters
        -----------
            size: Optional[Literal["tiny", "small", "large", "original"]]
                Size of the cover image
        """
        try: 
            return self.cover_image.get(_size, None)
        except AttributeError:
            return None

    def get_poster_image(
        self, size: 
        Optional[Literal["tiny", "small", "medium", "large", "original"]] = "original"
    ) -> Optional[str]:
        """Get the cover image

        Parameters
        -----------
            size: Optional[Literal["tiny", "small", "medium", "large", "original"]]
                Size of the poster image
        """
        try: 
            return self.poster_image.get(size, None)
        except AttributeError:
            return None

    @property
    def url(self) -> str:
        return f"https://kitsu.io/{self.entry_type}/{self.slug}"

    @property
    async def categories(self) -> List[Category]:
        async with self._session.get(
            url=f"{BASE}/{self.entry_type}/{self.id}/categories"
        ) as data:
            fetched_data = await data.json()
            categories = [Category(attributes) for attributes in fetched_data["data"]]
            return categories

class Category:
    """
    Represent a category of a media.

    Attributes
    ------------
    created_at: :class:`datetime`
    updated_at: :class:`datetime`
    title: :class:`str`
        Title of the category
    description: :class:`str`   
        Description of the category
    slug: :class:`str`
        Identifier string of the category
    nsfw: :class:`bool`
        If the category is NSFW or not
    """
    
    __slots__ = ('created_at', 'updated_at', 'title', 'description', 'slug', 'nsfw')

    def __init__(self, attributes: dict) -> None:
        data = attributes['attributes']
        self.created_at: datetime = datetime.strptime(data['createdAt'], "%Y-%m-%dT%H:%M:%S.%fZ") if (
            data['createdAt']) else None
        self.updated_at: datetime = datetime.strptime(data['updatedAt'], "%Y-%m-%dT%H:%M:%S.%fZ") if (
            data['updatedAt']) else None
        self.title: str = data['title']
        self.description: str = data['description']
        self.slug: str = data['slug']
        self.nsfw: bool = data['nsfw']

class Review:
    """Represents a :class:`Review` instance.
    Reviews belong to a media (:class:`Anime`, :class:`Manga`) 

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

    __slots__ = ('id', 'content', 'content_formatted', 'likes_count', 'progress',
                'rating', 'source', 'spoiler', 'media_id', 'media_type')

    def __init__(self, entry_id: str, entry_type: str, attributes: dict) -> None:
        data = attributes['attributes']
        self.media_id = entry_id 
        self.media_type = entry_type
        self.id: str = attributes['id']
        self.content: str = data['content']
        self.content_formatted: str = data['contentFormatted']
        self.likes_count: int = data['likesCount']
        self.progress: str = data['progress']
        self.rating: int = data['rating']
        self.source: str = data['source']
        self.spoiler: bool = data['spoiler']