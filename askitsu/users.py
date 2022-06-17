from datetime import datetime
import aiohttp
from typing import Optional
from .http import HTTPClient
from .images import CoverImage, Image

class User:

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
        self.id: int = attributes["id"]
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
        self.title: str = self._data["title"]
        self.profile_completed: bool = self._data["profileCompleted"]
        self.feed_completed: bool = self._data["feedCompleted"]
        self.sfw_filter: str = self._data["sfwFilterPreference"]

    @property
    def past_names(self) -> Optional[list]:
        names = self._data["pastNames"]
        return names if names else None

    @property
    def birthday(self) -> Optional[datetime]:
        try:
            return datetime.strptime(self._data["birthday"], "%Y-%m-%d")
        except ValueError:
            return None
    
    @property
    def avatar(self) -> Image:
        avatar = self._data["avatar"]
        if avatar:
            return Image(
                avatar
            )
        else:
            None
    
    @property
    def cover_image(self) -> Optional[CoverImage]:
        cover = self._data["coverImage"]
        if cover:
            return CoverImage(
                cover,
                entry_id=self.id,
                entry_type=self.entry_type
            )
        else:
            return None
