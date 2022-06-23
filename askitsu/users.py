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

from datetime import datetime
from typing import List, Optional

from .http import HTTPClient
from .images import CoverImage, Image
from .queries import BASE_URL, USERS_BY_ID_SOCIAL


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
        # "url",
        "_attributes",
        "_http"
    )

    def __init__(self, attributes: dict, http: HTTPClient) -> None:
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
        # self.url: str = attributes["url"]

    def __repr__(self) -> str:
        return f"<User slug='{self.slug}' id={self.id}"

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
        if avatar:
            return Image(
                avatar
            )
        else:
            None
    
    @property
    def cover_image(self) -> Optional[CoverImage]:
        """Background of the user profile"""
        cover = self._attributes["bannerImage"]
        if cover:
            return CoverImage(
                cover,
                entry_id=self.id,
                entry_type=self.entry_type
            )
        return None

    @property
    def banner(self) -> Optional[CoverImage]:
        """Same as :meth:`cover_image`"""
        return self.cover_image

    @property
    async def profile_links(self) -> Optional[List[UserProfile]]:
        """Social linked to the profile"""
        variables = {"id" : self.id}
        data = await self._http.post_data(
            url=BASE_URL,
            data = {"query" : USERS_BY_ID_SOCIAL, "variables" : variables}
        )
        try:
            return [
                UserProfile(attributes, self.slug)
                for attributes in data["data"]["findProfileById"]["siteLinks"]["nodes"]
            ]
        except KeyError:
            return None



class UserProfile:
    def __init__(self, attributes: dict, user: str) -> None:
        self._attributes = attributes
        self.id: int = int(attributes["id"])
        #self.name: str = _["attributes"]["name"]
        self.user: str = user
        self.url: str = attributes["url"]

    def __repr__(self) -> str:
        return f"<UserProfile id={self.id} slug={self.user}>"

    @property
    def created_at(self) -> Optional[datetime]:
        try:
            return datetime.strptime(self._attributes["createdAt"], "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError:
            return None

    @property
    def updated_at(self) -> Optional[datetime]:
        try:
            return datetime.strptime(self._attributes["updatedAt"], "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError:
            return None
