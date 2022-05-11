<h1 align="center">
    askitsu
</h1>

[![TwitterShomy](https://img.shields.io/badge/-shomykohai-1DA1F2?style=flat&logo=twitter&logoColor=white&labelColor=1DA1F2)](https://twitter.com/shomykohai)
[![askitsu](https://img.shields.io/pypi/v/askitsu?label=askitsu&logo=pypi&logoColor=white&labelColor=blue&color=9cf)](https://pypi.org/project/askitsu/)
[![Documentation Status](https://readthedocs.org/projects/askitsu/badge/?version=latest)](https://askitsu.readthedocs.io/en/latest/?badge=latest)

An async python wrapper for Kitsu.io API

# Key features

- Fully typed
- Use of `async` and `await`

# Installing

Requires python 3.8+

To install the package, you can simply run

```py
#Linux/MacOS
python3 -m pip install askitsu

#Windows
py -3 -m pip install askitsu
```

Or to get the latest commit

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
    anime = client.search_anime("attack on titan")
    print(anime.episode_count)
    print(anime.status)
    client.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(search())
```

More examples can be found inside the example directory -> [Here](https://github.com/ShomyKohai/askitsu/tree/master/examples)

# Links

- [Docs](https://askitsu.readthedocs.io/)
- [PyPi](https://pypi.org/project/askitsu/)
- [Kitsu.io Docs](https://kitsu.docs.apiary.io/)
- [discord.py](https://github.com/Rapptz/discord.py) (for docstrings inspiration and bot example)
