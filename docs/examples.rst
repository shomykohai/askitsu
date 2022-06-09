:orphan:
Examples
=============

In this section you will see various examples about library usage


Initializing client and search anime
-------------------------------------

.. code:: python
    
    import askitsu
    import asyncio

    client = askitsu.Client()

After initializing the client, you can start searching something
To do it, you'll have to make an async function

.. code:: python

    import askitsu
    import asyncio

    client = askitsu.Client()    

    async def main():
        anime = await client.search_anime('aot')
        print(anime.title)
        print(anime.episode_count)
        print(anime.youtube_url)
        await client.close()

And last we'll execute it using asyncio

.. code:: python

    import askitsu
    import asyncio

    client = askitsu.Client()    

    async def main():
        anime = await client.search_anime('aot')
        print(anime.title)
        print(anime.episode_count)
        print(anime.youtube_url)
        await client.close()

    if __name__ == '__main__':
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())


This will print out 

.. code:: 

    Attack on Titan
    25
    https://www.youtube.com/watch?v=LHtdKWJdif4

Fetch characters
----------------------

To fetch characters we'll start by using the previous code as a reference;
We will make a function that takes in input a name of an anime and returns a
list of characters

.. code:: python

    import askitsu
    import asyncio

    client = askitsu.Client()

    async def main(title: str = None):
        anime = await client.search_anime(title)
        characters = await anime.characters
        await client.close()
        return characters

    if __name__ == '__main__':
        anime_name = input("Search any anime: ")
        loop = asyncio.get_event_loop()
        characters = loop.run_until_complete(main(anime_name))
        for char in characters:
            print(char.name)

This will give as output all the characters (max 20) of the given anime

.. code::

    >>> Search any anime: aot
    Marlo Freudenberg
    Armin Arlert
    Eren Yeager
    Mother Ackerman
    Father Ackerman
    Grandfather Arlert
    Balto
    Moblit Berner
    Sasha Blouse
    Marco Bott
    ...


More examples can be found in examples directory at the `github repository <https://github.com/ShomyKohai/askitsu/tree/master/examples>`_
