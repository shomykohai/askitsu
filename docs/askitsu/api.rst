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
   :members: episodes, categories
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
   :members: chapters, categories
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
   :members:

Reviews
---------------------

.. autoclass:: askitsu.Review
   :members:

Titles
---------------------
.. autoclass:: askitsu.Title
   :members:

Assets
===============
Image
---------------------
.. autoclass:: askitsu.Image
   :members:

CoverImage
---------------------
.. autoclass:: askitsu.CoverImage
   :members:

PosterImage
---------------------
.. autoclass:: askitsu.PosterImage
   :members:

Errors
==============

AskitsuException
------------------------
.. ..autoexception:: askitsu.AskitsuException
   :members:
   :undoc-members:

HTTPError
------------------------
.. autoexception:: askitsu.HTTPError
   :members:
   :undoc-members:

InvalidArgument
------------------------
.. autoexception:: askitsu.InvalidArgument
   :members:
   :undoc-members:

NotAuthenticated
------------------------
.. autoexception:: askitsu.NotAuthenticated
   :members:
   :undoc-members:

BadApiRequest
------------------------
.. autoexception:: askitsu.BadApiRequest
   :members:
   :undoc-members:
