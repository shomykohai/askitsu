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

from typing import Literal, Optional, Union


__all__ = ("Image", "PosterImage", "CoverImage")


def get_dimension(dim: str, values: dict, value: str = "url") -> Optional[Union[str, int]]:
    for dimensions in values:
        if dim in dimensions.values():
            try:
                return dimensions.get(value, None)
            except (KeyError, TypeError):
                return None
    return None


class Image:
    """
    Represent a general image

    Attributes
    ---------------
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
            return get_dimension("tiny", self._data["views"])
        except (KeyError, TypeError):
            return None

    @property
    def small(self) -> Optional[str]:
        try:
            return get_dimension("small", self._data["views"])
        except (KeyError, TypeError):
            return None

    @property
    def medium(self) -> Optional[str]:
        try:
            return get_dimension("medium", self._data["views"])
        except (KeyError, TypeError):
            return None

    @property
    def large(self) -> Optional[str]:
        try:
            return get_dimension("large", self._data["views"])
        except (KeyError, TypeError):
            return None

    @property
    def original(self) -> Optional[str]:
        try:
            return self._data["original"].get("url", None)
        except (KeyError, TypeError):
            return None


class PosterImage(Image):
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

    def __init__(
        self, data: dict, entry_id: int = None, entry_type: str = None
    ) -> None:
        self._data = data
        self.entry_id = entry_id
        self.entry_type = entry_type

    def dimension(
        self, size: Literal["tiny", "small", "medium", "large"]
    ) -> Optional[dict]:
        try:
            width = get_dimension(size, self._data["views"], value="width")
            height = get_dimension(size, self._data["views"], value="height")
            return {"width" : width, "height" : height}
        except (KeyError, TypeError):
            return None


class CoverImage(Image):
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
    large: :class:`str`
        Cover image -- size: large
    original: :class:`str`
        Cover image with original size
    """

    def __init__(
        self, data: dict, entry_id: int = None, entry_type: str = None
    ) -> None:
        self._data = data
        self.entry_id = entry_id
        self.entry_type = entry_type

    @property
    def medium(self) -> None: #placeholder
        return None

    def dimension(
        self, size: Literal["tiny", "small", "medium", "large"]
    ) -> Optional[dict]:
        try:
            width = get_dimension(size, self._data["views"], value="width")
            height = get_dimension(size, self._data["views"], value="height")
            return {"width" : width, "height" : height}
        except (KeyError, TypeError):
            return None
