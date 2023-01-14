from enum import Enum

class MediaType(Enum):
    ANIME: str = "ANIME"
    MANGA: str = "MANGA" 

class LibraryEntryStatus(Enum):
    CURRENT: str = "CURRENT"
    PLANNED: str = "PLANNED"
    COMPLETED: str = "COMPLETED"
    ON_HOLD: str = "ON_HOLD"
    DROPPED: str = "DROPPED"