import base64
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord.ext import tasks
import random
import os
from dotenv import load_dotenv
import asyncio
from mcstatus import JavaServer
from craiyon import Craiyon, craiyon_utils
import time
from io import BytesIO
from PIL import Image
import stats.trackstats as trackstats

load_dotenv()

#enables custom help command
async def help(ctx):
    with open("config/help.txt", "r") as f:
        await ctx.send(f.read())

async def ping(ctx, bot):
    await ctx.send("Checking Servers...")
    try:
        server = JavaServer.lookup(os.getenv("MINECRAFT_SERVER"))
        status = server.status()
        await ctx.send(f"```The Minecraft server has {status.players.online} players and replied in {round(status.latency*100)} ms\n\nThe bot latency is " + str(round(bot.latency * 1000)) + "ms```")
    except:
        await ctx.send("Minecraft server is offline")
        await ctx.send("```The bot latency is " + str(round(bot.latency * 1000)) + "ms```")
        
async def mock(ctx):
    channel = ctx.channel
    history = [message async for message in channel.history(limit=2)] #get last 2 messages
    content = history[1].content
    for i in range(len(content)):
        if i % 2 == 0:
            content = content[:i] + content[i].upper() + content[i+1:]
    await channel.send(content)

#generates and image using the craiyon api and sends it to the chat
async def generate(ctx, *, prompt: str):
    await ctx.send(f"Generating prompt \"{prompt}\"...")
    generator = Craiyon() # Instantiates the api wrapper
    result = await generator.async_generate(prompt)
    b64_list = await craiyon_utils.async_encode_base64(result.images)    
    images1 = []
    for index, image in enumerate(b64_list): # Loop through b64_list, keeping track of the index
        img_bytes = BytesIO(base64.b64decode(image)) # Decode the image and store it as a bytes object
        image = discord.File(img_bytes)
        image.filename = f"result{index}.webp"
        images1.append(image) # Add the image to the images1 list 
    await ctx.reply(files=images1) # Reply to the user with all 9 images in 1 message
    
async def games(ctx, bot, *arg):
    print(arg.__len__())
    if arg.__len__() == 0:
        await ctx.send("```Games:\n .games - list all games\n .games <game> - play a game```")
    elif arg[0] == "gamble" and arg.__len__() == 2:
        if arg[1].isnumeric():
            await ctx.send("Rolling...")
            await asyncio.sleep(2)
            amount = random.randint(1, 10)
            await ctx.send("You rolled a " + str(amount))
            if amount == 1:
                await ctx.send("You lost 100 social credit")
                await trackstats.modifyUserLevel(ctx.author.id, )
            else:
                await ctx.send("You won " + str(amount) + " social credit")
                await trackstats.modifyUserLevel(ctx.author.id, amount)
        else:
            await ctx.send("Please enter a valid amount")
