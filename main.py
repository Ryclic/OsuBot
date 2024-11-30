import discord
import asyncio
import re
import requests
import io
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
async def rmap(ctx, difficulty=None):
    print("[Finding Random Map]")
    beatmap = find_random_map().beatmaps[-1].url
    await ctx.reply(beatmap)
    print("[Random Map Sent]")
    
@bot.command()
async def bgtrivia(ctx, difficulty=1, shared="no"):
    print("[Selecting Random Map]")
    challenge_map = select_map(difficulty)
    challenge_image = challenge_map.covers.cover_2x
    # Get rid of (TV Size) headers, etc for better matching
    map_title = re.sub(r'\[[^\]]*\]|\([^)]*\)', '', challenge_map.title).lower().strip()

    embed = discord.Embed(title="What map is this background from?")
    embed.set_image(url=challenge_image)
    embed.set_footer(text="Difficulty Level: " + str(difficulty) + ", Timeout: 30 seconds")

    await ctx.reply(embed=embed)
    print("[Map Challenge Sent: " + map_title + "]")

    def check(m):
        if shared == "yes":
            if m.channel == ctx.channel:
                if m.content == "skip":
                    raise NotImplementedError()
                elif fuzz.ratio(map_title, m.content) >= 50:
                    return True
                else:
                    return False
        else:
            if m.channel == ctx.channel and m.author.id == ctx.author.id:
                if m.content == "skip":
                    raise NotImplementedError()
                elif fuzz.ratio(map_title, m.content) >= 50:
                    return True
                else:
                    return False
            
    try:
        await bot.wait_for("message", timeout=30.0, check=check)
    except asyncio.TimeoutError:
        await ctx.reply("You ran out of time! The map was: **" + map_title + "** \n" + challenge_map.beatmaps[-1].url)
    except NotImplementedError:
        await ctx.reply("You skipped the question! The map was: **" + map_title + "** \n" + challenge_map.beatmaps[-1].url)
    else:
        await ctx.reply("That's correct! The map was: **" + map_title + "** \n" + challenge_map.beatmaps[-1].url)

@bot.command()
async def strivia(ctx, difficulty=1, shared="no"):
    print("[Selecting Random Map]")
    challenge_map = select_map(difficulty)
    challenge_mp3_url = "https://" + challenge_map.preview_url[2:]
    mp3_data = None
    # Store the mp3 in memory
    try:
        response = requests.get(challenge_mp3_url)
        if response.status_code == 200:
            mp3_data = io.BytesIO(response.content)
        else:
            print("MP3 was not able to be saved!")
    except Exception as e:
        print(e)
        print("MP3 fetch request failed!")

    # Get rid of (TV Size) headers, etc for better matching
    map_title = re.sub(r'\[[^\]]*\]|\([^)]*\)', '', challenge_map.title).lower().strip()

    embed = discord.Embed(title="What map uses this song?")
    embed.set_footer(text="Difficulty Level: " + str(difficulty) + ", Timeout: 30 seconds")

    await ctx.reply(embed=embed)
    await ctx.reply(file=discord.File(mp3_data, filename="song.mp3"))
    print("[Map Challenge Sent: " + map_title + "]")

    def check(m):
        if shared == "yes":
            if m.channel == ctx.channel:
                if m.content == "skip":
                    raise NotImplementedError()
                elif fuzz.ratio(map_title, m.content) >= 50:
                    return True
                else:
                    return False
        else:
            if m.channel == ctx.channel and m.author.id == ctx.author.id:
                if m.content == "skip":
                    raise NotImplementedError()
                elif fuzz.ratio(map_title, m.content) >= 50:
                    return True
                else:
                    return False

    try:
        await bot.wait_for("message", timeout=30.0, check=check)
    except asyncio.TimeoutError:
        await ctx.reply("You ran out of time! The map was: **" + map_title + "** \n" + challenge_map.beatmaps[-1].url)
    except NotImplementedError:
        await ctx.reply("You skipped the question! The map was: **" + map_title + "** \n" + challenge_map.beatmaps[-1].url)
    else:
        await ctx.reply("That's correct! The map was: **" + map_title + "** \n" + challenge_map.beatmaps[-1].url)

bot.run(DISCORD_KEY)

