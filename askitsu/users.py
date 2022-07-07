from __future__ import annotations

from datetime import datetime
from typing import List, Optional
from .http import HTTPClient
from .images import CoverImage, Image

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
    likes_given: :class:`int`
        Number of likes given by the user
    likes_received: :class:`int`
        Number of likes received by the user
    posts_count: :class:`int`
        Number of posts
    rating_count: :class:`int`
        Number of ratings made by the user
    media_reaction: :class:`int`
        Number of interaction with medias
    pro: :class:`bool`
        Return if the user has pro tier
    status: :class:`str`
        Status of the user (if they're registered or not)
    title: Optional[:class:`str`]
        Title of the user (if has one)
        Example: "Staff"
    profile_completed: :class:`bool`
        Return if the user has completed his profile
    feed_completed: :class:`bool`
        If the user completed their feed
    sfw_filter: :class:`str`
        Current SFW filter of the user
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
        "likes_given",
        "likes_received",
        "posts_count",
        "rating_count",
        "media_reaction",
        "pro",
        "status",
        "title",
        "profile_completed",
        "feed_completed",
        "sfw_filter",
        "_data",
        "_http",
    )

    def __init__(self, attributes: dict, http: HTTPClient) -> None:
        self._http = http
        self._data = attributes["attributes"]
        self.id: int = int(attributes["id"])
        self.entry_type: str = "users"
        self.name: str = self._data["name"]
        self.slug: str = self._data["slug"]
        self.about: str = self._data["about"]
        self.location: Optional[str] = self._data["location"]
        self.waifu_husbando: str = self._data["waifuOrHusbando"]
        self.followers: int = self._data["followersCount"]
        self.following: int = self._data["followingCount"]
        self.gender: Optional[str] = self._data["gender"]
        self.comments_count: int = self._data["commentsCount"]
        self.favorites_count: int = self._data["favoritesCount"]
        self.likes_given: int = self._data["likesGivenCount"]
        self.likes_received: int = self._data["likesReceivedCount"]
        self.posts_count: int = self._data["postsCount"]
        self.rating_count: int = self._data["ratingsCount"]
        self.media_reaction: int = self._data["mediaReactionsCount"]
        self.pro: bool = True if self._data["proTier"] else False
        self.status: str = self._data["status"]
        self.title: Optional[str] = self._data["title"]
        self.profile_completed: bool = self._data["profileCompleted"]
        self.feed_completed: bool = self._data["feedCompleted"]
        self.sfw_filter: str = self._data["sfwFilterPreference"]

    def __repr__(self) -> str:
        return f"<User slug='{self.slug}' id={self.id}"

    @property
    def past_names(self) -> Optional[list]:
        """Past names of the user (if avaiable)"""
        names = self._data["pastNames"]
        return names if names else None

    @property
    def birthday(self) -> Optional[datetime]:
        """Birthday of the user (if set)"""
        try:
            return datetime.strptime(self._data["birthday"], "%Y-%m-%d")
        except TypeError:
            return None

    @property
    def avatar(self) -> Optional[Image]:
        """Avatar of the user"""
        avatar = self._data["avatar"]
        if avatar:
            return Image(avatar)
        else:
            return None

    @property
    def banner(self) -> Optional[CoverImage]:
        """Background of the user profile"""
        cover = self._data["coverImage"]
        if cover:
            return CoverImage(cover, entry_id=self.id, entry_type=self.entry_type)
        else:
            return None

    @property
    def url(self) -> str:
        return f"https://kitsu.io/users/{self.slug}"

    @property
    async def profile_links(self) -> Optional[List[UserProfile]]:
        data = await self._http.get_data(
            url=f"users/{self.id}/profile-links?include=profileLinkSite"
        )
        return [
            UserProfile(attributes["id"], attributes["attributes"], self.slug, included)
            for attributes, included in zip(data["data"], data["included"])
        ]


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

    def __init__(self, id: int, attributes: dict, user: str, included: dict) -> None:
        self._attributes = attributes
        self.id: int = int(id)
        self.name: str = included["attributes"]["name"]
        self.user: str = user
        self.url: str = attributes["url"]

    def __repr__(self) -> str:
        return f"<UserProfile id={self.id} slug={self.user}>"

    @property
    def created_at(self) -> Optional[datetime]:
        """When the user added the link to their profile"""
        try:
            return datetime.strptime(
                self._attributes["createdAt"], "%Y-%m-%dT%H:%M:%S.%fZ"
            )
        except ValueError:
            return None

    @property
    def updated_at(self) -> Optional[datetime]:
        """When the user last updated the link"""
        try:
            return datetime.strptime(
                self._attributes["updatedAt"], "%Y-%m-%dT%H:%M:%S.%fZ"
            )
        except ValueError:
            return None
