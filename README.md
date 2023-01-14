<h1  align="center">
askitsu
</h1>

[![TwitterShomy](https://img.shields.io/badge/-shomykohai-1DA1F2?style=flat&logo=twitter&logoColor=white&labelColor=1DA1F2)](https://twitter.com/shomykohai)
[![askitsu](https://img.shields.io/pypi/v/askitsu?label=askitsu&logo=pypi&logoColor=white&labelColor=blue&color=9cf)](https://pypi.org/project/askitsu/)
[![Documentation Status](https://readthedocs.org/projects/askitsu/badge/?version=master)](https://askitsu.readthedocs.io/en/master/?badge=master)

<p align="center">
  An async wrapper for Kitsu.io API written in Python
</p>

![askitsu](https://github.com/ShomyKohai/askitsu/blob/master/docs/images/dark.png?raw=true "askitsu")
  

# IMPORTANT

💡 UPDATE:<br>
The master branch is now in a status where it can be used.<br>
For any issue you may encounter, please make a new [issue](https://github.com/ShomyKohai/askitsu/issues).<br>
You can check the [projects](https://github.com/ShomyKohai/askitsu/projects?type=classic) tab to see current proggress.

⚠️ askitsu is going trough a rewrite to support the new Kitsu GraphQL API<br>
Therefore this branch is not currently ready to be used.<br>
If you wish to use the library, please install the `json-api` branch.

# Key features

- Fully typed
- Use of `async`/`await`
- Support most of primary Kitsu entries -- Anime, Manga, Characters and much more
- Can be used with discord bots

# Currently avaiable endpoints

- 🎞️ Anime (Anime, Episodes and Streaming Links)
- 📖 Manga (Manga and Chapters)
- 👥 Characters
- 📰 Reviews
- 👤 User (Profile and Profile Links)
- 🗞️ Posts
- 📚 User Libraries

Coming soon:

- 🗨️ Comments

# Installing

Requires python 3.8+

To install the package, you can simply run

```py

#Linux/MacOS
python3 -m pip install askitsu


#Windows
py -3 -m pip install askitsu

```

Or to get the latest dev version

```py

#Linux/MacOS
python3 -m pip install git+https://github.com/ShomyKohai/askitsu.git

  

#Windows
py -3 -m pip install git+https://github.com/ShomyKohai/askitsu.git

```

## Requirements

- [aiohttp](https://pypi.org/project/aiohttp/)
- [colorama](https://pypi.org/project/colorama/)

# Examples

```py
import askitsu
import asyncio

async def search():
    client = askitsu.Client()
    anime = await client.search_anime("attack on titan")
    print(anime.episode_count)
    print(anime.status)
    await client.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(search())

```

More examples can be found inside the example directory -> [Here](https://github.com/ShomyKohai/askitsu/tree/master/examples)

# Links & Credits

- [Docs](https://askitsu.readthedocs.io/)
- [PyPi](https://pypi.org/project/askitsu/)
- [Kitsu.io Docs](https://kitsu.io/api/playground)
- [discord.py](https://github.com/Rapptz/discord.py) (bot example)

__"Kitsu" name and the "Kitsu logo" are property of [Kitsu](https://kitsu.io/)__
