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
from typing import Optional, Literal

class Character:
    """Represents a :class:`Character` istance

    Attributes
    -----------
    media_id: :class:`int`
        ID of the character's origin media
    id: :class:`int`
        ID of the character
    name: :class:`str`
        Return characters canonical name
    slug: :class:`str`
        String identifier. Work as id to fetch data
    description: :class:`str`
        The character's description
    role: Literal[:class:`str`]
        Role of the character ("main" or "supporting")
    mal_id: :class:`int`
        Character ID on My Anime List
    image: :class:`str`
        Return character's image
    created_at: Optional[:class:`datetime`]
    updated_at: Optional[:class:`datetime`]
    """       

    __slots__ = ('id', 'media_id', 'name', 'slug', 'description', 'role',
                'slug', 'mal_id', 'image', 'created_at', 'updated_at')

    def __init__(self, entry_id: str, data: dict):
        self.media_id = entry_id
        attributes = data['attributes']
        self.id: str = data['id']
        self.name: str = attributes['canonicalName']
        self.description: str = attributes['description']
        self.role: Literal["main", "supporting"] = None
        self.slug: str = attributes['slug']
        self.mal_id: str = attributes['malId']
        self.created_at: datetime = datetime.strptime(attributes['createdAt'], "%Y-%m-%dT%H:%M:%S.%fZ") if (
            attributes['createdAt']) else None
        self.updated_at: datetime = datetime.strptime(attributes['updatedAt'], "%Y-%m-%dT%H:%M:%S.%fZ") if (
            attributes['updatedAt']) else None
        self.image: str = attributes['image']


    @classmethod
    async def _character_instance(
            cls, 
            link: str = None,
            _cls = None, 
            entry_id: str = None, 
            role: Literal["main", "supporting"] = None
    ) -> Character:
        _data = await _cls._get_data(url=link)
        _character = Character(entry_id, _data["data"])
        _character.role = role
        return _character

    def get_image(self, _size: 
        Optional[Literal["tiny", "small", "medium", "large", "original"]] = "original"
    ) -> Optional[str]:
        try: 
            return self.image.get(_size, None)
        except AttributeError:
            return None
        