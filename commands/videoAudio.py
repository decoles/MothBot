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
from selenium import webdriver
from bs4 import BeautifulSoup

#add a pause command
#add a resume command

queue = []

async def scrapeVideoData(url):
    driver = webdriver.Chrome()
    driver.get('{}/videos?view=0&sort=p&flow=grid'.format(url))
    content = driver.page_source.encode('utf-8').strip()
    soup = BeautifulSoup(content, 'lxml')
    titles = soup.findAll('a', id='video-title')
    views = soup.findAll(
        'span', class_='style-scope ytd-grid-video-renderer')
    video_urls = soup.findAll('a', id='video-title')
    print('Channel: {}'.format(url))
    i = 0  # views and time
    j = 0  # urls
    for title in titles[:10]:
        print('\n{}\t{}\t{}\thttps://www.youtube.com{}'.format(title.text,
                                                                views[i].text, views[i+1].text, video_urls[j].get('href')))
        i += 2
        j += 1
 
async def pause(ctx, bot): #pauses audio NOT WORKING
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if(voice.is_playing()):
        voice.pause()
    else:
        await ctx.send("Nothing is playing")

async def resume(ctx, bot): #resumes audio NOT WORKING
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if(voice.is_paused()):
        voice.resume()
    else:
        await ctx.send("Nothing is paused")

async def stop(ctx, bot): #stops audio and clears queue
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    try:
        if voice.is_playing():
            voice.stop()
            queue.clear()
            await ctx.voice_client.disconnect()
        else:
            await ctx.send("Nothing is playing")
    except:
        await ctx.send("Nothing is playing")

async def skip(ctx, bot):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    try:
        if voice.is_playing():
            voice.stop()
        else:
            await ctx.send("Nothing is playing")
    except:
        await ctx.send("Nothing is playing")


async def play(ctx, *, prompt: str, bot):
    if (prompt.startswith("https://www.youtube.com/watch?v=")
        or prompt.startswith("https://youtu.be")
        or prompt.startswith("https://m.youtube.com")):
        if ctx.voice_client and ctx.author.voice and ctx.voice_client.channel == ctx.author.voice.channel and ctx.voice_client.is_playing():
            await ctx.send("Added to queue")
            queue.append(prompt)
        if(ctx.author.voice): #if user is in voice channel
            channel = ctx.message.author.voice.channel #get Message Sender Channel. When you want it to join without a seperat function.
            if not(ctx.voice_client): #if bot is not in voice channel prevents double join 
                voice = await channel.connect(reconnect=True)
            else:
                voice = ctx.voice_client
            if not ctx.voice_client.is_playing(): #if bot is not playing start prevents a double feed of queue
                url = prompt #gets video url
                ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
                ydl_opts = {'format': 'bestaudio/best', 'noplaylist':'True'}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    song_info = ydl.extract_info(url, download=False)
                voice.play(discord.FFmpegOpusAudio(song_info["url"], **ffmpeg_options)) #play audio
                while voice.is_playing():
                    await asyncio.sleep(1) #wait for sound to finish
                if(len(queue) > 0):
                    await ctx.send("Playing next song in queue")
                    await play(ctx, prompt=queue.pop(0), bot=bot)
                else:
                    if ctx.voice_client:
                        await ctx.voice_client.disconnect()
        else:
            await ctx.send("Not in voice channel")
    else:
        await ctx.send("Please enter a valid youtube link")

async def viewQueue(ctx):
    if(len(queue) > 0):
        val = "```"
        await ctx.send("Queue:")
        for i in range(len(queue)):
            # await ctx.send(queue[i])
            #tempstr = await scrapeVideoData(queue[i])
            val += str(i+1) + ". " + queue[i] + "\n"
        val += "```"
        await ctx.send(val)

    else:
        await ctx.send("Queue is empty")