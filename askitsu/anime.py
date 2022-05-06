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

__all__ = ('Anime', 'StreamLink')

from .core import Entry
from typing import Optional


class Anime(Entry):
    """Represents an :class:`Anime` instance 

    Attributes
    -----------
    id: :class:`int`
        ID of the anime
    status: :class:`str`
        Actual status of the given anime (Ex. "finished")
    created_at: Optional[:class:`datetime`]
    updated_at: Optional[:class:`datetime`]
    started_at: Optional[:class:`datetime`]
    ended_at: Optional[:class:`datetime`]
    slug: :class:`str`
        String identifier. Work as id to fetch data
    synopsis: :class:`str`
        Description of the given anime
    title: :class:`str`
        Return canon title of the given anime
    episode_count: :class:`int`
        Episode number
    episode_lenght: :class:`int`
        Lenght of a single episode of the anime
    total_lenght: :class:`int`
        Total lenght of all episodes (minutes)
    nsfw: :class:`bool`
        Check if the anime is NSFW or SFW
        Return True | False
    yt_id: :class:`str`
        Return id of the YouTube trailer
    cover_image: :class:`str`
        Return cover image
    poster_image: :class:`str`
        Return poster image
    rating_rank: :class:`int`
        Return rating rank
    popularity_rank: :class:`int`
        Return popularity rank position
    youtube_url: Optional[:class:`str`]
        Return full url of YouTube trailer
    """

    __slots__ = (
        'id', 'type', 'status', 'created_at', 'updated_at', 'started_at', 'ended_at',
        'slug', 'synopsis', 'title', 'episode_count', 'episode_length', 'total_length',
        'nsfw', 'yt_id', 'cover_image', 'poster_image', 'rating_rank', 'popularity_rank'
    )

    def __init__(self, type: str, attributes: dict, *args):
        data = attributes['attributes']
        self.type = "anime"
        self.episode_count: int = data['episodeCount']
        self.episode_length: int = data['episodeLength']
        self.total_length: int = data['totalLength']
        self.nsfw: bool = data['nsfw']
        self.yt_id: str = data['youtubeVideoId']
        super().__init__(attributes['id'], type, data, *args)

    @property
    def youtube_url(self) -> Optional[str]:
        return f"https://www.youtube.com/watch?v={self.yt_id}" if self.yt_id else None


class StreamLink():

    __slots__ = ('id', 'url', 'subs', 'dub')

    def __init__(self, attributes: dict):
        data = attributes['attributes']
        self.id: int = attributes['id']
        self.url: str = data['url']
        self.subs: list = data['subs']
        self.dub: list = data['dubs']

class Episodes:
    pass