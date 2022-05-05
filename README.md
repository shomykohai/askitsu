<h1 align="center">
    askitsu
</h1>

[![TwitterShomy](https://img.shields.io/badge/-shomykohai-1DA1F2?style=flat&logo=twitter&logoColor=white&labelColor=1DA1F2)](https://twitter.com/shomykohai)

An async python wrapper for Kitsu.io API

# Key features

- Fully typed
- Use of `async` and `await`

# Installing

Requires python 3.8+

To install the package, you can simply run

```py
#Linux/MacOS
python3 -m pip install git+https://github.com/ShomyKohai/askitsu.git

#Windows
py -3 -m pip install git+https://github.com/ShomyKohai/askitsu.git
```

## Requirements

- [aiohttp](https://pypi.org/project/aiohttp/)

# Examples

```py
import askitsu
import asyncio

async def search():
    client = askitsu.Client()
    anime = client.search_anime("attack on titan")
    print(anime.episode_cout)
    print(anime.status)
    client.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(search())
```

More examples can be found inside the example directory -> [Here](https://github.com/ShomyKohai/askitsu/tree/master/examples)