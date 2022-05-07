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
