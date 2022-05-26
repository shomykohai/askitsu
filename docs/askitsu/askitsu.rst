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

Entries
===============

Anime
--------------------

.. autoclass:: askitsu.Anime
   :members: get_cover_image, get_poster_image
   :show-inheritance:

StreamingLinks
--------------------
.. autoclass:: askitsu.StreamLink
   :members:

Manga
--------------------

.. autoclass:: askitsu.Manga
   :members: get_cover_image, get_poster_image
   :show-inheritance:

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
