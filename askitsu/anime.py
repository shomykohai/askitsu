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

from datetime import datetime
from typing import List, Optional, Union

from .core import Entry
from .http import HTTPClient


class StreamLink:
    """
    Represent an :class:`Anime` stream link
    (where you can watch the anime)


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

    def __init__(self, attributes: dict, included: dict):
        data = attributes["attributes"]
        self.id: int = int(attributes["id"])
        self.name: str = included["siteName"]
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
        "synopsis",
        "description",
        "title",
        "season",
        "number",
        "length",
        "thumbnail",
        "_attributes",
    )

    def __init__(self, attributes: dict) -> None:
        self._attributes = attributes["attributes"]
        self.id: int = int(attributes["id"])
        self.synopsis: str = self._attributes["synopsis"]
        self.description: str = self._attributes["description"]
        self.title: str = self._attributes["canonicalTitle"]
        self.season: int = self._attributes["seasonNumber"]
        self.number: int = self._attributes["number"]
        self.length: int = self._attributes["length"]
        self.thumbnail: str = (
            self._attributes["thumbnail"]["original"]
            if self._attributes["thumbnail"]
            else None
        )

    @property
    def created_at(self) -> Optional[datetime]:
        """Date when this episode got added on Kitsu"""
        try:
            return datetime.strptime(
                self._attributes["createdAt"], "%Y-%m-%dT%H:%M:%S.%fZ"
            )
        except ValueError:
            return None

    @property
    def updated_at(self) -> Optional[datetime]:
        """Last time when this episode got updated on Kitu"""
        try:
            return datetime.strptime(
                self._attributes["updatedAt"], "%Y-%m-%dT%H:%M:%S.%fZ"
            )
        except ValueError:
            return None


class Anime(Entry):
    """Represents an :class:`Anime` instance

    Attributes
    -----------
    id: :class:`int`
        ID of the anime
    status: :class:`str`
        Actual status of the given anime (E.g. "finished")
    slug: :class:`str`
        String identifier. Work as id to fetch data
    synopsis: :class:`str`
        Description of the given anime
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
    rating_rank: :class:`int`
        Return rating rank (Position on the leaderboard based on rating)
    popularity_rank: :class:`int`
        Return popularity rank (Position on the leaderboard based on user preferences)
    rating: :class:`float`
        The rating received from the community in a scale from 1 to 100

        .. versionadded:: 0.4.0

    age_rating: Literal['G', 'PG', 'R', 'R18']
        Age rating of the anime

        .. versionadded:: 0.4.0

    subtype: Literal['ONA', 'OVA', 'TV', 'movie', 'music', 'special']
        The subtype of the show

        .. versionadded:: 0.4.1
    """

    __slots__ = (
        "id",
        "entry_type",
        "status",
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
        "_http",
        "_titles",
        "_attributes",
    )

    def __init__(self, attributes: dict, http: HTTPClient, *args) -> None:
        data = attributes["attributes"]
        self._http = http
        self.entry_type = "anime"
        self.episode_count: int = data["episodeCount"]
        self.episode_length: int = data["episodeLength"]
        self.total_length: int = data["totalLength"]
        self.nsfw: bool = data["nsfw"]
        self.yt_id: str = data["youtubeVideoId"]
        super().__init__(attributes["id"], self.entry_type, data, http, *args)

    def __repr__(self) -> str:
        return f"<Anime name='{self.canonical_title}' id={self.id}>"

    @property
    def youtube_url(self) -> Optional[str]:
        """Return full url of YouTube trailer"""
        return f"https://www.youtube.com/watch?v={self.yt_id}" if self.yt_id else None

    @property
    async def stream_links(self) -> Optional[List[StreamLink]]:
        """
        Return a list of :class:`StreamLink`

        .. versionadded:: 0.4.0
        """
        data = await self._http.get_data(
            url=f"anime/{self.id}/streaming-links?include=streamer"
        )
        try:
            return [
                StreamLink(links, included["attributes"])
                for links, included in zip(data["data"], data["included"])
            ]
        except KeyError:
            return []

    async def episodes(self, limit: int = 12) -> Union[Episode, List[Episode]]:
        """
        Returns an episode or a list of episodes

        .. versionadded:: 0.4.0

        limit: :class:`int`
            Limit of episodes to fetch. Defaults to 12 (Max 25).
        """
        data = await self._http.get_data(
            url=f"anime/{self.id}/episodes?page[limit]={limit}"
        )
        episodes = [Episode(attributes) for attributes in data["data"]]
        return episodes if len(episodes) > 1 else episodes[0]
