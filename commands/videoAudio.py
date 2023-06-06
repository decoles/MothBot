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

#create a queue for songs
#add a skip command
#add a queue command
#add a pause command
#add a resume command

queue = []

async def stop(ctx, bot):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    try:
        if voice.is_playing():
            voice.stop()
        else:
            await ctx.send("Nothing is playing")
    except:
        await ctx.send("Nothing is playing")

async def play(ctx, *, prompt: str):
    if (prompt.startswith("https://www.youtube.com/watch?v=") or prompt.startswith("https://youtu.be") or prompt.startswith("https://m.youtube.com")):
        if(ctx.author.voice): #if user is in voice channel
            channel = ctx.message.author.voice.channel #get Message Sender Channel. When you want it to join without a seperat function.
            voice = await channel.connect(reconnect=True)
            url = prompt #gets video url
            ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
            ydl_opts = {'format': 'bestaudio/best', 'noplaylist':'True'}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                song_info = ydl.extract_info(url, download=False)
            ctx.voice_client.play(discord.FFmpegOpusAudio(song_info["url"], **ffmpeg_options)) #play audio
            while voice.is_playing():
                await asyncio.sleep(1) #wait for sound to finish
            await ctx.voice_client.disconnect() #Go to server then go to voice client and remove it
        else:
            await ctx.send("Not in voice channel")
    else:
        await ctx.send("Please enter a valid youtube link")
        
async def addToQueue():
    pass