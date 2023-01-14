from enum import Enum
from typing import Literal


class Entries(Enum):
    ANIME: str = "anime"
    MANGA: str = "manga"
    CHARACTER: str = "character"


Media = Literal[Entries.ANIME, Entries.MANGA]
Fetchable = Literal[Entries.ANIME, Entries.MANGA, Entries.CHARACTER]


class MediaType(Enum):
    ANIME: str = "ANIME"
    MANGA: str = "MANGA"


class LibraryEntryStatus(Enum):
    CURRENT: str = "CURRENT"
    PLANNED: str = "PLANNED"
    COMPLETED: str = "COMPLETED"
    ON_HOLD: str = "ON_HOLD"
    DROPPED: str = "DROPPED"
