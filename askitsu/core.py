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
from typing import Optional, Literal

class Entry:

    __slots__ = ('id', 'type', 'status', 'created_at', 'updated_at', 'started_at', 'ended_at',
                'slug', 'synopsis', 'title', 'rating_rank', 'popularity_rank')

    def __init__(self, id: str, type: str, attributes: dict):
        self.id= id
        self.type = type
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


    def get_cover_image(
        self, 
        _size: Optional[Literal["tiny", "small", "large", "original"]] = "original"
    ) -> Optional[str]:
        try: 
            return self.cover_image.get(_size, None)
        except AttributeError:
            return None

    def get_poster_image(
        self, _size: 
        Optional[Literal["tiny", "small", "medium", "large", "original"]] = "original"
    ) -> Optional[str]:
        try: 
            return self.poster_image.get(_size, None)
        except AttributeError:
            return None
