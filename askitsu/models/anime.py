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
    ANIME_BY_ID_CATEGORIES,
    ANIME_BY_ID_CHARACTERS,
    ANIME_BY_ID_EPISODES,
    ANIME_BY_ID_REVIEWS,
    ANIME_BY_ID_STREAMLINKS,
    BASE_URL
)


__all__ = ("Anime", "StreamLink", "Episode")


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
    name: :class:`str`
        Name of the stream service
    """

    __slots__ = ("id", "url", "subs", "dub", "name")

    def __init__(self, attributes: dict):
        self.id: int = int(attributes["id"])
        self.name: str = attributes["streamer"]["siteName"]
        self.url: str = attributes["url"]
        self.subs: list = attributes["subs"]
        self.dub: list = attributes["dubs"]


class Episode:
    """
    Represent an :class:`Anime` episode

    .. versionadded:: 0.4.0

    Attributes
    -----------
    id: :class:`int`
        ID of the episode
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
        "description",
        "title",
        "season",
        "number",
        "length",
        "thumbnail",
        "_attributes"
    )

    def __init__(self, attributes: dict) -> None:
        self.id: int = int(attributes["id"])
        self.description: str = attributes["description"]
        self.title: str = attributes["titles"]["canonical"]
        self.number: int = attributes["number"]
        self.length: int = attributes["length"]
        self.thumbnail: str = attributes["thumbnail"]["original"]["url"]

    @property
    def created_at(self) -> Optional[datetime]:
        """Date when this episode got added on Kitsu"""
        try:
            return datetime.strptime(self._attributes["createdAt"], "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            return None

    @property
    def updated_at(self) -> Optional[datetime]:
        """Last time when this episode got updated on Kitu"""
        try:
            return datetime.strptime(self._attributes["updatedAt"], "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            return None


class Anime(Entry):
    """Represents an :class:`Anime` instance

    Attributes
    -----------
    id: :class:`int`
        ID of the anime
    status: :class:`str`
        Actual status of the given anime (Ex. "finished"
    started_at: Optional[:class:`datetime`]
        Date when the anime started
    ended_at: Optional[:class:`datetime`]
        Date when the anime ended
    slug: :class:`str`
        String identifier. Work as id to fetch data
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
        "slug",
        "description",
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
        "_http",
        "_titles",
        "_attributes",
        "_cache"
    )

    def __init__(self, attributes: dict, http: HTTPClient, cache: Cache, *args) -> None:
        self.entry_type = "anime"
        self.episode_count: int = attributes["episodeCount"]
        self.episode_length: int = attributes["episodeLength"]
        self.total_length: int = attributes["totalLength"]
        self.nsfw: bool = not attributes["sfw"]
        self.yt_id: Optional[str] = attributes["youtubeTrailerVideoId"]
        self.subtype: str = attributes["animesub"]
        super().__init__(
            _id=attributes["id"],
            _type=self.entry_type,
            attributes=attributes,
            http=http,
            cache=cache,
            *args
        )

    def __repr__(self) -> str:
        return f"<Anime name='{self.canonical_title}' id={self.id}>"

    @property
    def youtube_url(self) -> Optional[str]:
        return f"https://www.youtube.com/watch?v={self.yt_id}" if self.yt_id else None

    @property
    async def stream_links(self) -> Optional[List[StreamLink]]:
        cache_res = await self._cache.get(f"anime_{self.id}_streamlinks")
        if cache_res:
            return cache_res.value
        variables = {"id" : self.id}
        data = await self._http.post_data(
            url=BASE_URL,
            data={"query" : ANIME_BY_ID_STREAMLINKS, "variables" : variables}

        )
        try:
            links = [
                StreamLink(attributes=attributes) 
                for attributes in data["data"]["findAnimeById"]["streamingLinks"]["nodes"]
            ]
            await self._cache.add(f"anime_{self.id}_streamlinks", links)
            return links
        except KeyError:
            return None

    @property
    async def categories(self) -> List[Category]:
        cache_res = await self._cache.get(f"anime_{self.id}_categories")
        if cache_res:
            return cache_res.value
        variables = {"id" : self.id}
        data = await self._http.post_data(
            url=BASE_URL,
            data={"query" : ANIME_BY_ID_CATEGORIES, "variables" : variables}
        )
        categories =  [
            Category(attributes)
            for attributes in data["data"]["findAnimeById"]["categories"]["nodes"]
        ]
        await self._cache.add(
            f"anime_{self.id}_categories",
            categories,
            remove_after=self._cache.expiration       
        )
        return categories

    @property
    async def characters(self) -> List[Character]:
        cache_res = await self._cache.get(f"anime_{self.id}_characters")
        if cache_res:
            return cache_res.value
        variables = {"id" : self.id, "limit" : 100}
        data = await self._http.post_data(
            url=BASE_URL,
            data={"query" : ANIME_BY_ID_CHARACTERS, "variables" : variables}
        )
        characters = [
            Character(attributes, entry_id=self.id)
            for attributes in data["data"]["findAnimeById"]["characters"]["nodes"]
        ]
        await self._cache.add(
            f"anime_{self.id}_characters",
            characters,
            remove_after=self._cache.expiration
        )
        return characters


    async def reviews(self, limit: int = 1) -> List[Review]:
        variables = {"id" : self.id, "limit" : limit}
        data = await self._http.post_data(
            url=BASE_URL,
            data={"query" : ANIME_BY_ID_REVIEWS, "variables" : variables}
        )
        return [
            Review(self.id, self.entry_type, attributes)
            for attributes in data["data"]["findAnimeById"]["reactions"]["nodes"]
        ]

    async def episodes(self, limit: int = 12) -> List[Episode]:
        """
        Returns a list of episodes

        .. versionadded:: 0.4.0

        limit: :class:`int`
            Limit of episodes to fetch. Defaults to 12.
        """
        cache_res = await self._cache.get(f"anime_{self.id}_episodes_{limit}")
        if cache_res:
            return cache_res.value
        variables = {"id" : self.id, "limit" : limit}
        data = await self._http.post_data(
            url=BASE_URL,
            data={"query" : ANIME_BY_ID_EPISODES, "variables" : variables}
        )
        episodes = [Episode(attributes) for attributes in data["data"]["findAnimeById"]["episodes"]["nodes"]]
        await self._cache.add(
            f"anime_{self.id}_episodes_{limit}",
            episodes,
            remove_after=self._cache.expiration
        )
        return episodes

