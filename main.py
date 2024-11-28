import discord
from random_map import *
from secrets_storage import *

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    # Avoid anything by own bot
    if message.author == client.user:
        return
    # Get a random map
    if message.content.startswith('$mapr'):
        print("[Finding Random Map]")
        beatmap = find_random_map().beatmaps[-1].url
        await message.channel.send(beatmap)
        print("[Random Map Sent]")
    # Get a trivia question
client.run(DISCORD_KEY)

