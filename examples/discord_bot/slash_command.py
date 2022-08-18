import askitsu
import asyncio
import discord

"""

For more examples about slash commands and how they work see
the discord.py official repository
https://github.com/Rapptz/discord.py/blob/master/examples/app_commands/

"""


# Without subclassing Client

TOKEN = "place token here"

intents = discord.Intents.default()
client = discord.Client(intents=intents)
client.tree = discord.app_commands.CommandTree(client)
kitsu = askitsu.Client()

@client.tree.command()
async def anime(interaction: discord.Interaction, *, query: str) -> None:
    query_formatted = query.replace(" ", "+")
    anime = await kitsu.search_anime(query_formatted)
    await interaction.response.send_message(f"Anime: {anime.title}\nEpisodes: {anime.episode_count}")
    await kitsu.close()

client.run(TOKEN)
