import askitsu
import asyncio

async def search_anime(name: str) -> askitsu.Anime:
    client = askitsu.Client()
    data = await client.search_anime(name, limit=1)
    await client.close()
    return data


if __name__ == '__main__':
    name = input("Search anime: ")
    fetch = asyncio.run(search_anime(name))
    print(
        f"""
        Anime name: {fetch.title}
        Status: {fetch.status}
        ID: {fetch.id}
        YouTube URL: {fetch.youtube_url}
        """
    )