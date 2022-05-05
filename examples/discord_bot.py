import askitsu
import asyncio
import discord
from discord.ext import commands

TOKEN = "place token here"

intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(
    command_prefix="!", 
    intents=intents
    )


@bot.event
async def on_ready() -> None:
    print("Ready.")

@bot.command(name="anime")
async def _anime(ctx, *, query: str) -> None:
    query_formatted = query.replace(" ", "+")
    kitsu = askitsu.Client()
    anime = await kitsu.search_anime(query_formatted, limit=1)
    await ctx.send(f"Anime: {anime.title}\nEpisodes: {anime.episode_count}")
    await kitsu.close()


asyncio.run(bot.start(TOKEN))