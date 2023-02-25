"""
Async Kitsu API Wrapper
~~~~~~~~~~~~~~~~~~~~~~~~

Simple & asynchronus wrapper for the Kitsu API
Written in python

:copyright: (c) 2022-present ShomyKohai
:license: MIT, see LICENSE

"""

__title__ = "askitsu"
__author__ = "ShomyKohai"
__license__ = "MIT"
__copyright__ = "Copyright 2022-present ShomyKohai"
__version__ = "1.0.0"

# __all__

from .client import *
from .error import *
from .models.anime import *
from .models.character import *
from .models.core import *
from .models.enums import *
from .models.images import *
from .models.manga import *
from .models.users import *
