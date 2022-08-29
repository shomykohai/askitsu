askitsu
===================================

.. image:: images/dark.png
   :class: only-dark

.. image:: images/light.png
   :class: only-light

IMPORTANT
==========

| ⚠️ askitsu is going trough a rewrite to support the new Kitsu GraphQL API
| Therefore this branch is not currently ready to be used.
| If you wish to use the library, please install the `master` branch.

`Features`
   * askitsu is an async API wrapper written in python for `Kitsu.io <https://kitsu.io/>`_.
   * It offers access to various endpoints such :class:`Anime`.
   * Written with ``async``/``await`` syntax
   * Compatible with discord bots (See examples)

`Overview of the features`

.. tab-set::

      .. tab-item:: Supported endpoints
         * 🎞️ Anime (Anime, Episodes and Streaming Links)
         * 📖 Manga (Manga and Chapters)
         * 👥 Characters
         * 📰 Reviews
         * 👤 User (Profile and Profile Links)

      .. tab-item:: Coming Soon
         * 🗞️ Posts
         * 🗨️ Comments
         * 📚 User Libraries

Introduction
==================
To begin with askitsu you can read the guides below
   * **First steps** to work with the library: :doc:`Introduction <../introduction>` | :doc:`Token <../token>`
   * **Simple examples** to get started with the library: :doc:`Examples <../examples>`
   * **API Reference** :doc:`API <../askitsu/api>`


Tree
-----------------
* :ref:`genindex`
* :ref:`search`


.. toctree:: 
   :hidden:
   :caption: Contents:

   introduction
   token
   examples

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: API Reference:

   modules
