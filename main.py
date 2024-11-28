import discord
from discord.ext import commands
from random_map import *
from secrets_storage import *

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}!')

@bot.command()
async def mapr(ctx, arg=None):
    print("[Finding Random Map]")
    beatmap = find_random_map().beatmaps[-1].url
    await ctx.send(beatmap)
    print("[Random Map Sent]")
    
bot.run(DISCORD_KEY)

