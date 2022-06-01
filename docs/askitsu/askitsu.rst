Info
===============

.. automodule:: askitsu
   :members:
   :undoc-members:

Core
===============

Client
---------------------

.. autoclass:: askitsu.Client
   :members:

Anime
===============

Anime
--------------------

.. autoclass:: askitsu.Anime
   :members: get_cover_image, get_poster_image, categories
   :show-inheritance:

Episode
--------------------
.. autoclass:: askitsu.Episode
   :members:

StreamingLinks
--------------------
.. autoclass:: askitsu.StreamLink
   :members:

Manga
==============

Manga
--------------------

.. autoclass:: askitsu.Manga
   :members: get_cover_image, get_poster_image, categories
   :show-inheritance:

Chapter
--------------------
.. autoclass:: askitsu.Chapter
   :members:


Misc
================

Categories
---------------------

.. autoclass:: askitsu.Category
   :members:


Character
------------------------

.. autoclass:: askitsu.Character
   :members: get_image

Reviews
---------------------

.. autoclass:: askitsu.Review
   :members:

Errors
==============

AskitsuException
------------------------
.. autoclass:: askitsu.AskitsuException
   :members:
   :undoc-members:

HTTPError
------------------------
.. autoclass:: askitsu.HTTPError
   :members:
   :undoc-members:

InvalidArgument
------------------------
.. autoclass:: askitsu.InvalidArgument
   :members:
   :undoc-members:

NotAuthenticated
------------------------
.. autoclass:: askitsu.NotAuthenticated
   :members:
   :undoc-members:

BadApiRequest
------------------------
.. autoclass:: askitsu.BadApiRequest
   :members:
   :undoc-members:
