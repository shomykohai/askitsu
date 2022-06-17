from datetime import datetime
import aiohttp
from typing import Optional
from .http import HTTPClient
from .images import CoverImage, Image

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
        ...
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
        ...
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
        "_data"
    )

    def __init__(self, attributes: dict) -> None:
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
            return Image(
                avatar
            )
        else:
            None
    
    @property
    def cover_image(self) -> Optional[CoverImage]:
        """Background of the user profile"""
        cover = self._data["coverImage"]
        if cover:
            return CoverImage(
                cover,
                entry_id=self.id,
                entry_type=self.entry_type
            )
        else:
            return None
