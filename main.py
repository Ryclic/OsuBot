import discord
import asyncio
import re
from discord.ext import commands
from randmap import *
from trivia import *
from secrets_storage import *
from rapidfuzz import fuzz

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}!")

@bot.command()
async def rmap(ctx, arg=None):
    print("[Finding Random Map]")
    beatmap = find_random_map().beatmaps[-1].url
    await ctx.send(beatmap)
    print("[Random Map Sent]")
    
@bot.command()
async def bgtrivia(ctx, arg=1):
    print("[Selecting Random Map]")
    challenge_map = select_map(arg)
    challenge_image = challenge_map.covers.cover_2x
    # Get rid of (TV Size) headers, etc for better matching
    map_title = re.sub(r'\[[^\]]*\]|\([^)]*\)', '', challenge_map.title).lower().strip()

    embed = discord.Embed(title="What map is this background from?")
    embed.set_image(url=challenge_image)
    embed.set_footer(text="Difficulty Level: " + str(arg) + ", Timeout: 10 seconds")

    await ctx.send(embed=embed)
    print("[Map Challenge Sent: " + map_title + "]")

    def check(m):
        if m.channel == ctx.channel and m.author.id == ctx.author.id:
            if fuzz.ratio(map_title, m.content) >= 50:
                return True
            else:
                return False
    try:
        await bot.wait_for("message", timeout=10.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send("You ran out of time! The map was: **" + map_title + "** \n" + challenge_map.beatmaps[-1].url)
    else:
        await ctx.send("That's correct!")
        

bot.run(DISCORD_KEY)

