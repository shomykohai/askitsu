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

__all__ = ("Anime", "StreamLink", "Episode")

import aiohttp
from datetime import datetime
from typing import List, Optional, Union
from .core import Entry, BASE


class StreamLink:
    """
    Represent an :class:`Anime` stream link


    Attributes
    -----------
    id: :class:`int`
        ID of Anime Stream links
    url: :class:`str`
        URL of streaming service
    subs: :class:`list`
        Avaiable subs
    dub: :class:`list`
        Avaiable dub in streaming service
    """

    __slots__ = ("id", "url", "subs", "dub")

    def __init__(self, attributes: dict):
        data = attributes["attributes"]
        self.id: int = int(attributes["id"])
        self.url: str = data["url"]
        self.subs: list = data["subs"]
        self.dub: list = data["dubs"]


class Episode:
    """
    Represent an :class:`Anime` episode

    .. versionadded:: 0.4.0

    Attributes
    -----------
    id: :class:`int`
        ID of the episode
    created_at: Optional[:class:`datetime`]
    updated_at: Optional[:class:`datetime`]
    synopsis: :class:`str`
        Synopsis of the episode
    description: :class:`str`
        Full description of the episode
    title: :class:`str`
        Title of the episode
    season: :class:`int`
        Season which the episode belong to
    number: :class:`int`
        Episode's number
    lenght: :class:`int`
        Lenght of the episode (in minutes)
    thumbnail: :class:`str`
        Url of the thumbnail
    """

    __slots__ = (
        "id",
        "created_at",
        "updated_at",
        "synopsis",
        "description",
        "title",
        "season",
        "number",
        "length",
        "thumbnail",
    )

    def __init__(self, attributes: dict) -> None:
        data = attributes["attributes"]
        self.id: int = int(attributes["id"])
        self.created_at: Optional[datetime] = (
            datetime.strptime(data["createdAt"], "%Y-%m-%dT%H:%M:%S.%fZ")
            if (data["createdAt"])
            else None
        )
        self.updated_at: Optional[datetime] = (
            datetime.strptime(data["updatedAt"], "%Y-%m-%dT%H:%M:%S.%fZ")
            if (data["updatedAt"])
            else None
        )
        self.synopsis: str = data["synopsis"]
        self.description: str = data["description"]
        self.title: str = data["canonicalTitle"]
        self.season: int = data["seasonNumber"]
        self.number: int = data["number"]
        self.length: int = data["length"]
        self.thumbnail: str = (
            data["thumbnail"]["original"] if data["thumbnail"] else None
        )


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

        .. versionchanged:: 0.4.1

        Now it returns an instance of :class:`askitsu.Title`
    canonical_title: :class:`str`
        Returns canonical title of the given anime

        .. versionadded:: 0.4.1

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
    cover_image: :class:`CoverImage`
        Return cover image dict with all sizes

        .. versionchanged:: 0.4.1

        Now it returns a cover image object

    poster_image: :class:`PosterImage`
        Return poster image dict with all sizes

        .. versionchanged:: 0.4.1

        Now it returns a poster image object

    rating_rank: :class:`int`
        Return rating rank (Position on the leaderboard based on rating)
    popularity_rank: :class:`int`
        Return popularity rank (Position on the leaderboard based on user preferences)
    youtube_url: Optional[:class:`str`]
        Return full url of YouTube trailer
    url: :class:`str`
        Returns url to Kitsu.io website

        .. versionadded:: 0.4.0

    stream_links: List[:class:`StreamLink`]
        Return a list of :class:StreamLink

        .. versionadded:: 0.4.0

    rating: :class:`float`
        The rating received from the community in a scale from 1 to 100

        .. versionadded:: 0.4.0

    age_rating: Literal['G', 'PG', 'R', 'R18']
        Age rating of the anime

        .. versionadded:: 0.4.0

    categories: List[:class:`Category`]
        Categories of the anime

        .. versionadded:: 0.4.0

    subtype: Literal['ONA', 'OVA', 'TV', 'movie', 'music', 'special']
        The subtype of the show

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
        "created_at",
        "updated_at",
        "started_at",
        "ended_at",
        "slug",
        "synopsis",
        "canonical_title",
        "episode_count",
        "episode_length",
        "total_length",
        "nsfw",
        "yt_id",
        "rating_rank",
        "popularity_rank",
        "rating",
        "age_rating",
        "subtype",
        "_session",
        "_titles",
        "_attributes"
    )

    def __init__(self, attributes: dict, session: aiohttp.ClientSession, *args) -> None:
        data = attributes["attributes"]
        self._session = session
        self.entry_type = "anime"
        self.episode_count: int = data["episodeCount"]
        self.episode_length: int = data["episodeLength"]
        self.total_length: int = data["totalLength"]
        self.nsfw: bool = data["nsfw"]
        self.yt_id: str = data["youtubeVideoId"]
        super().__init__(attributes["id"], self.entry_type, data, session, *args)

    @property
    def youtube_url(self) -> Optional[str]:
        return f"https://www.youtube.com/watch?v={self.yt_id}" if self.yt_id else None

    async def _fetch_stream_links(self) -> Optional[List[StreamLink]]:
        async with self._session.get(
            url=f"{BASE}/anime/{self.id}/streaming-links"
        ) as data:
            fetched_data = await data.json()
            return (
                [StreamLink(links) for links in fetched_data["data"]]
                if fetched_data
                else None
            )

    @property
    async def stream_links(self) -> Optional[List[StreamLink]]:
        return await self._fetch_stream_links()

    async def episodes(self, limit: int = 12) -> Union[Episode, List[Episode]]:
        """
        Returns a a episode or a list of episodes

        .. versionadded:: 0.4.0

        limit: :class:`int`
            Limit of episodes to fetch. Defaults to 12 (Max 25).
        """
        async with self._session.get(
            url=f"{BASE}/anime/{self.id}/episodes?page[limit]={limit}"
        ) as data:
            fetched_data = await data.json()
            episodes = [Episode(attributes) for attributes in fetched_data["data"]]
            return episodes if len(episodes) > 1 else episodes[0]
