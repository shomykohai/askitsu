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

from colorama import Fore, Style  # type: ignore
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Union

from .anime import Anime
from .enums import Entries, MediaType, LibraryEntryStatus
from .images import CoverImage, Image
from .manga import Manga
from ..cache import Cache
from ..error import InvalidArgument, NotFound
from ..http import HTTPClient
from ..queries import USERS_BY_ID_SOCIAL, USER_LIBRARY, POSTS_FROM_USER


__all__ = ("User", "UserProfile")


class User:
    """
    Represents a user of Kitsu

    .. versionadded:: 0.5.0

    Attributes
    ---------------
    id: :class:`int`
        The id of the user
    name: :class:`str`
        Name of the user
    slug: :class:`str`
        String identifier of the user (nickname)
    about: :class:`str`
        About section of the user (description)
    location: Optional[:class:`str`]
        Location of the user (if set)
    waifu_husbando: :class:`str`
        Return the choice of the user if they have a
        waifu or an husbando
    followers: :class:`int`
        Followers count of the users
    following: :class:`int`
        Number of users that the user is following
    gender: Optional[:class:`str`]
        Gender of the user (if set)
    comments_count: :class:`int`
        Number of comment posted by the user
    favorites_count: :class:`int`
        Number of favorites media of the user
    posts_count: :class:`int`
        Number of posts
    media_reaction: :class:`int`
        Number of interaction with medias
    pro: :class:`bool`
        Return if the user has pro tier
    pro_tier: Optional[:class:`str`]
        Return the typology of pro
    """

    __slots__ = (
        "id",
        "entry_type",
        "name",
        "slug",
        "about",
        "location",
        "waifu_husbando",
        "followers",
        "following",
        "gender",
        "comments_count",
        "favorites_count",
        "posts_count",
        "media_reaction",
        "pro",
        "pro_tier",
        "_attributes",
        "_http",
        "_cache",
    )

    def __init__(self, attributes: dict, http: HTTPClient, cache: Cache) -> None:
        self._cache = cache
        self._http = http
        self._attributes = attributes
        self.id: int = int(attributes["id"])
        self.entry_type: str = "users"
        self.name: str = attributes["name"]
        self.slug: str = attributes["slug"]
        self.about: str = attributes["about"]
        self.location: Optional[str] = attributes["location"]
        self.waifu_husbando: Optional[str] = attributes["waifuOrHusbando"]
        self.followers: int = attributes["followers"]["totalCount"]
        self.following: int = attributes["following"]["totalCount"]
        self.gender: Optional[str] = attributes["gender"]
        self.comments_count: int = attributes["comments"]["totalCount"]
        self.favorites_count: int = attributes["favorites"]["totalCount"]
        self.posts_count: int = attributes["posts"]["totalCount"]
        self.media_reaction: int = attributes["mediaReactions"]["totalCount"]
        self.pro: bool = True if attributes["proTier"] else False
        self.pro_tier: Optional[str] = attributes["proTier"]

    def __repr__(self) -> str:
        return f"<User slug='{self.slug}' id={self.id}>"

    @property
    def url(self) -> str:
        return f"https://kitsu.io/users/{self.slug}"

    @property
    def birthday(self) -> Optional[datetime]:
        """Birthday of the user (if set)"""
        try:
            return datetime.strptime(self._attributes["birthday"], "%Y-%m-%d")
        except TypeError:
            return None

    @property
    def avatar(self) -> Optional[Image]:
        """Avatar of the user"""
        avatar = self._attributes["avatarImage"]
        return Image(avatar) if avatar else None

    @property
    def cover_image(self) -> Optional[CoverImage]:
        """Background of the user profile"""
        cover = self._attributes["bannerImage"]
        return (
            CoverImage(cover, entry_id=self.id, entry_type=self.entry_type)
            if cover
            else None
        )

    @property
    def banner(self) -> Optional[CoverImage]:
        """Same as :meth:`cover_image`"""
        return self.cover_image

    @property
    async def profile_links(self) -> Optional[List[UserProfile]]:
        """Social linked to the profile"""
        cache_res = await self._cache.get(f"user_{self.slug}_profilelinks")
        if cache_res:
            return cache_res.value
        variables = {"id": self.id}
        data = await self._http.post_data(
            data={"query": USERS_BY_ID_SOCIAL, "variables": variables}
        )
        try:
            links = [
                UserProfile(attributes, self.slug)
                for attributes in data["data"]["findProfileById"]["siteLinks"]["nodes"]
            ]
            await self._cache.add(
                f"user_{self.slug}_profilelinks",
                links,
                remove_after=self._cache.expiration,
            )
            return links
        except KeyError:
            return None

    async def library_entries_count(self, media: MediaType) -> int:
        query = """
            query library_entries_count ($id: ID!, $media: MediaTypeEnum!) {
                findProfileById(id: $id) {
                    library{
                        all(mediaType: $media, first: 2000){
                            totalCount
                        }
                    }
                }
            }
        """
        variables = {"id": self.id, "media": str(media.value).upper()}
        data = await self._http.post_data(data={"query": query, "variables": variables})
        return data["data"]["findProfileById"]["library"]["all"].get("totalCount", 0)

    @property
    def created_at(self) -> Optional[datetime]:
        """When the user registered to Kitsu"""
        try:
            return datetime.strptime(
                self._attributes["createdAt"], "%Y-%m-%dT%H:%M:%SZ"
            )
        except ValueError:
            return None

    async def posts(self, limit: int = 10) -> Optional[List[Post]]:
        if limit > 2000:
            raise InvalidArgument(
                f"{Fore.RED}The argument {Fore.YELLOW}`limit` {Fore.RED}can't exceed {Fore.LIGHTCYAN_EX}2000{Style.RESET_ALL}"
            )
        cache_res = await self._cache.get(f"user_{self.slug}_posts")
        if cache_res:
            return cache_res.value
        variables = {"id": self.id, "limit": limit}
        data = await self._http.post_data(
            data={"query": POSTS_FROM_USER, "variables": variables}
        )
        try:
            posts = [
                Post(attributes, self)
                for attributes in data["data"]["findProfileById"]["posts"]["nodes"]
            ]
            await self._cache.add(
                f"user_{self.slug}_posts",
                posts,
                remove_after=self._cache.expiration,
            )
            return posts
        except KeyError:
            return None

    async def library(
        self, media: MediaType, filter: LibraryEntryStatus = None, limit: int = 10
    ) -> Optional[List[LibraryEntry]]:
        if limit > 2000:
            raise InvalidArgument(
                f"{Fore.RED}The argument {Fore.YELLOW}`limit` {Fore.RED}can't exceed {Fore.LIGHTCYAN_EX}2000{Style.RESET_ALL}"
            )
        cache_res = await self._cache.get(
            f"user_{self.slug}_library_{media.value}_{limit}_{filter.value if filter else 'ALL'}"
        )
        if cache_res:
            return cache_res.value
        variables = {"media": str(media.value).upper(), "id": self.id, "limit": limit}
        query = USER_LIBRARY % f'{f", status: {filter.value}" if filter else ""}'
        data = await self._http.post_data(data={"query": query, "variables": variables})
        try:
            entries = [
                LibraryEntry(attributes, self, self._http)
                for attributes in data["data"]["findProfileById"]["library"]["all"][
                    "nodes"
                ]
            ]
            await self._cache.add(
                f"user_{self.slug}_library_{media.value}_{limit}_{filter.value if filter else 'ALL'}",
                entries,
                remove_after=self._cache.expiration,
            )
            return entries
        except KeyError:
            return None


@dataclass()
class UserProfile:
    """
    A profile linked to a :class:`User`

    Attributes
    ---------------
    id: :class:`int`
        The id of the profile link
    name: :class:`str`
        Name of the linked profile
    user: :class:`str`
        Name of the user whom the profile belong to
    url: :class:`str`
        The url to the profile of the user
    """

    def __init__(self, attributes: dict, user: str) -> None:
        self._attributes = attributes
        self.id: int = int(attributes["id"])
        self.name: str = attributes["site"]["name"]
        self.user: str = user
        self.url: str = attributes["url"]

    def __repr__(self) -> str:
        return f"<UserProfile id={self.id} slug={self.user}>"


class Post:
    """
    A post made by a :class:`User`

    Attributes
    -----------
    id: :class:`int`
        ID of the post
    content: :class:`str`
        Formatted content of the post
    nsfw: :class:`bool`
        If the post is marked as NSFW by the author
    likes_count: :class:`int`
        Number of likes in the post
    spoiler: :class:`bool`
        If the post is marked as spoiler by the author
    author: :class:`User`
        The author of the Post
    """

    def __init__(self, attributes: dict, author: User) -> None:
        self._attributes = attributes
        self.id: int = int(attributes["id"])
        self.content: str = attributes["content"]
        self.nsfw: bool = attributes["isNsfw"]
        self.spoiler: bool = attributes["isSpoiler"]
        self.likes_count: int = int(attributes["likes"]["totalCount"])
        self.author = author

    @property
    def created_at(self) -> Optional[datetime]:
        """When the user registered to Kitsu"""
        try:
            return datetime.strptime(
                self._attributes["createdAt"], "%Y-%m-%dT%H:%M:%SZ"
            )
        except ValueError:
            return None


class LibraryEntry:
    """
    A library entry that belongs to a :class:`User`

    Attributes
    -----------
    id: :class:`int`
        ID of the LibraryEntry
    status: :class:`LibraryEntryStatus`
        Status of the Media in the library entry
    user: :class:`User`
        User which the library entry belongs to
    reconsume_count: :class:`int`
        Number of reconsume of a media
        (E.g. Rewatch in `Anime`)
    reconsuming: :class:`bool`
        If the user is currently reconsuming the Media
    rating: Optional[:class:`int`]
        Rating of the Media given by the user
    private: :class:`bool`
        If the library entry is private
    progress: :class:`int`
        Progress of the user in the linked media
    media_type: :class:`str`
        The type of the linked media: `Anime` or `Manga`
    media_id: :class:`int`
        The ID of the linked media
    nsfw: :class:`bool`
        If the library entry is NSFW or not
    notes: Optional[class:`str`]
        Additional notes made by the user
    """

    def __init__(self, attributes: dict, user: User, http: HTTPClient) -> None:
        self.__http = http
        self._attributes = attributes
        self.media_type: str = attributes["media"]["type"]
        self.media_id: int = attributes["media"]["id"]
        self.id = int(attributes["id"])
        self.user: User = user
        self.progress: int = int(attributes["progress"])
        self.nsfw: bool = attributes["nsfw"]
        self.status: LibraryEntryStatus = attributes["status"]
        self.reconsume_count: int = attributes["reconsumeCount"]
        self.reconsuming: bool = attributes["reconsuming"]
        self.rating: Optional[int] = attributes["rating"]
        self.notes: Optional[str] = attributes["notes"]
        self.private: bool = attributes["private"]

    def __repr__(self) -> str:
        return f"<LibraryEntry id={self.id} type={self.media_type} media_id={self.media_id} user={self.user}>"

    @property
    async def media(self) -> Union[Anime, Manga]:
        """The linked media"""
        if self.media_type == MediaType.ANIME.value.capitalize():
            query = "findAnimeById"
        elif self.media_type == MediaType.MANGA.value.capitalize():
            query = "findMangaById"
        else:
            raise NotFound
        return await self.__http._get_entry_fetch(
            # Return media type as value of enum
            Entries(self.media_type.lower()),
            self.media_id,
            query,
        )

    @property
    def created_at(self) -> Optional[datetime]:
        """When the library entry got created"""
        try:
            return datetime.strptime(
                self._attributes["createdAt"], "%Y-%m-%dT%H:%M:%SZ"
            )
        except ValueError:
            return None

    @property
    def progressed_at(self) -> Optional[datetime]:
        """When the library entry got a progress update"""
        try:
            return datetime.strptime(
                self._attributes["progressedAt"], "%Y-%m-%dT%H:%M:%SZ"
            )
        except ValueError:
            return None

    @property
    def finished_at(self) -> Optional[datetime]:
        """When the library entry got finished"""
        try:
            return datetime.strptime(
                self._attributes["finishedAt"], "%Y-%m-%dT%H:%M:%SZ"
            )
        except ValueError:
            return None
