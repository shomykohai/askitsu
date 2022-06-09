import askitsu
import asyncio

async def characters(id: int = None) -> None:
    client = askitsu.Client()
    anime = await client.get_anime_entry(id)
    characters = await anime.characters
    for char in characters:
        print(char.name)
    await client.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(characters(3532))

