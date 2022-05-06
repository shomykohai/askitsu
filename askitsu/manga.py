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

__all__ = ('Manga')

from .core import Entry

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
        #Total lenght of all episodes (minutes)
    cover_image: :class:`str`
        Return cover image
    poster_image: :class:`str`
        Return poster image
    rating_rank: :class:`int`
        Return rating rank
    popularity_rank: :class:`int`
        Return popularity rank position
    """

    __slots__ = ('id', 'type', 'status', 'created_at', 'updated_at', 'started_at', 'ended_at',
                'slug', 'synopsis', 'title', 'cover_image', 'poster_image', 'rating_rank',
                'popularity_rank', 'chapter_count', 'volume_count', 'serialization',)

    def __init__(self, type: str, attributes: dict):
        data = attributes['attributes']
        self.type: str = "manga"
        self.chapter_count: int = data['chapterCount']
        self.volume_count: int = data['volumeCount']
        self.serialization: str = data['serialization']
        super().__init__(attributes['id'], type, data)