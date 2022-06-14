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

from typing import Literal, Optional

class Image:
    """
    Represent a general image

    Attributes
    ---------------
    entry_id: :class:`int`
        The id which the poster image belongs to
    entry_type: :class:`str`
        The type of the media
    tiny: :class:`str`
        Poster image -- size: tiny
    small: :class:`str`
        Poster image -- size: small
    medium: :class:`str`
        Poster image -- size: medium
    large: :class:`str`
        Poster image -- size: large
    original: :class:`str`
        Poster image with original size
    """

    def __init__(self, data: dict) -> None:
        self._data = data

    @property
    def tiny(self) -> Optional[str]:
        try:
            return self._data.get("tiny", None)
        except:
            return None
    
    @property
    def small(self) -> Optional[str]:
        try:
            return self._data.get("small", None)
        except:
            return None

    @property
    def medium(self) -> Optional[str]:
        try:
            return self._data.get("medium", None)
        except:
            return None

    @property
    def large(self) -> Optional[str]:
        try:
            return self._data.get("large", None)
        except:
            return None

    @property
    def original(self) -> Optional[str]:
        try:
            return self._data.get("original", None)
        except:
            return None

class PosterImage:
    """
    Poster image of a media

    Attributes
    ---------------
    entry_id: :class:`int`
        The id which the poster image belongs to
    entry_type: :class:`str`
        The type of the media
    tiny: :class:`str`
        Poster image -- size: tiny
    small: :class:`str`
        Poster image -- size: small
    medium: :class:`str`
        Poster image -- size: medium
    large: :class:`str`
        Poster image -- size: large
    original: :class:`str`
        Poster image with original size
    """

    def __init__(self, data: dict, entry_id: int = None, entry_type: str = None) -> None:
        self._data = data
        self.entry_id = entry_id
        self.entry_type = entry_type

    @property
    def tiny(self) -> Optional[str]:
        try:
            return self._data.get("tiny", None)
        except:
            return None
    
    @property
    def small(self) -> Optional[str]:
        try:
            return self._data.get("small", None)
        except:
            return None

    @property
    def medium(self) -> Optional[str]:
        try:
            return self._data.get("medium", None)
        except:
            return None

    @property
    def large(self) -> Optional[str]:
        try:
            return self._data.get("large", None)
        except:
            return None

    @property
    def original(self) -> Optional[str]:
        try:
            return self._data.get("original", None)
        except:
            return None

    def dimension(
        self, 
        size: Literal["tiny", "small", "medium", "large"]
    ) -> Optional[dict]:
        try:
            return self._data["meta"]["dimensions"][size]
        except:
            return None


class CoverImage:
    """
    Cover image of a media

    Attributes
    ---------------
    entry_id: :class:`int`
        The id which the cover image belongs to
    entry_type: :class:`str`
        The type of the media
    tiny: :class:`str`
        Cover image -- size: tiny
    small: :class:`str`
        Cover image -- size: small
    medium: :class:`str`
        Cover image -- size: medium
    large: :class:`str`
        Cover image -- size: large
    original: :class:`str`
        Cover image with original size
    """

    def __init__(self, data: dict, entry_id: int = None, entry_type: str = None) -> None:
        self._data = data
        self.entry_id = entry_id
        self.entry_type = entry_type

    @property
    def tiny(self) -> Optional[str]:
        try:
            return self._data.get("tiny", None)
        except:
            return None
    
    @property
    def small(self) -> Optional[str]:
        try:
            return self._data.get("small", None)
        except:
            return None

    @property
    def large(self) -> Optional[str]:
        try:
            return self._data.get("large", None)
        except:
            return None

    @property
    def original(self) -> Optional[str]:
        try:
            return self._data.get("original", None)
        except:
            return None

    def dimension(
        self, 
        size: Literal["tiny", "small", "large"]
    ) -> Optional[dict]:
        try:
            return self._data["meta"]["dimensions"][size]
        except:
            return None