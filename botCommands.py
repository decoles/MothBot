import base64
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord.ext import tasks
import random
import os
from dotenv import load_dotenv
import asyncio
import yt_dlp
from mcstatus import JavaServer
from craiyon import Craiyon
import time
from io import BytesIO
from PIL import Image
import trackstats

load_dotenv()

def soundList(): #get list of sounds from folder
    sounds = []
    for file in os.listdir("./sounds"):
        sounds.append(file)
    return sounds

async def stop(ctx, bot):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    try:
        if voice.is_playing():
            voice.stop()
        else:
            await ctx.send("Nothing is playing")
    except:
        await ctx.send("Nothing is playing")
    
#enables custom help command
async def help(ctx):
    await ctx.send("```detection:\n .detect <link> - identifies object in image\nsounds:\n .sounds - list all sounds\n .play <sound> - play sound\n .stop - stop playing sound\n\nother:\n .help - list all commands\n .ping - ping available servers!```")

async def sounds(ctx):
    await ctx.send("```Sounds:\n " + "\n ".join(soundList()) + "```")

async def play(ctx, *arg):
    try:
        if arg.__len__() == 0 or arg.__len__() > 1: #allows for some modularity
            await ctx.send("Please specify a sound or youtube link")
            return
        elif arg.__len__() == 1 and (arg[0].startswith("https://www.youtube.com/watch?v=") or arg[0].startswith("https://youtu.be") or arg[0].startswith("https://m.youtube.com")):
            if(ctx.author.voice): #if user is in voice channel
                channel = ctx.message.author.voice.channel #get Message Sender Channel. When you want it to join without a seperat function.
                voice = await channel.connect() #same applies to this
                url = arg[0]
                ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
                ydl_opts = {'format': 'bestaudio/best', 'noplaylist':'True'}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    song_info = ydl.extract_info(url, download=False)
                ctx.voice_client.play(discord.FFmpegOpusAudio(song_info["url"], **ffmpeg_options)) 
                while voice.is_playing():
                    await asyncio.sleep(1) #wait for sound to finish
                await ctx.voice_client.disconnect() #Go to server then go to voice client and remove it
            else:
                await ctx.send("Not in voice channel")

        elif arg[0] not in soundList():
            await ctx.send("Enter a valid sound or youtube link")
            return
        else:
            voice = None
            player = None
            if(ctx.author.voice): #if user is in voice channel
                channel = ctx.message.author.voice.channel
                voice = await channel.connect()
                source = FFmpegPCMAudio('./sounds/' + arg[0])
                player = voice.play(source)    
                while voice.is_playing():
                    await asyncio.sleep(1) #wait for sound to finish
                await ctx.guild.voice_client.disconnect() #Go to server then go to voice client and remove it
            else:
                await ctx.send("Not in voice channel")
    except:
        await ctx.send("Somethings already playing")

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

async def generate(ctx, arg):
    await ctx.send("Generating image... ETA: 50 seconds")
    generator = Craiyon() # Instantiates the api wrapper
    result = await generator.async_generate(arg)
    count = 0
    for i in result.images:
        count += 1 #incremnts image name
        byt = BytesIO()
        image = Image.open(BytesIO(base64.decodebytes(i.encode("utf-8"))))
        image.save(byt, 'PNG')
        byt.seek(0)
        await ctx.send(file=discord.File(fp=byt, filename=f"Image_{count +1}.png"))

    #await result.async_save_images()
    
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
