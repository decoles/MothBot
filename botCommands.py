import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import random
import os
from dotenv import load_dotenv
import asyncio
import yt_dlp

def soundList(): #get list of sounds from folder
    sounds = []
    for file in os.listdir("./sounds"):
        sounds.append(file)
    return sounds

async def stop(ctx, bot):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.stop()
        await ctx.guild.voice_client.disconnect() #Go to server then go to voice client and remove it
    else:
        await ctx.send("Nothing is playing")
    
#enables custom help command
async def help(ctx):
    await ctx.send("```sounds:\n .sounds - list all sounds\n .play <sound> - play sound\n .stop - stop playing sound\n\nother:\n .help - list all commands\n .ping - pong!```")

async def sounds(ctx):
    await ctx.send("```Sounds:\n " + "\n ".join(soundList()) + "```")

async def play(ctx, *arg):
    if arg.__len__() == 0 or arg.__len__() > 1:
        await ctx.send("Please specify a sound or youtube link")
        return
    elif arg.__len__() == 1 and arg[0].startswith("https://www.youtube.com/watch?v="):
        if(ctx.author.voice): #if user is in voice channel
            voiceChannel = ctx.message.author.voice.channel #get Message Sender Channel. When you want it to join without a seperat function.
            await voiceChannel.connect() #same applies to this
            url = arg[0]
            ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
            ydl_opts = {'format': 'bestaudio/best', 'noplaylist':'True'}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                song_info = ydl.extract_info(url, download=False)
            ctx.voice_client.play(discord.FFmpegOpusAudio(song_info["url"], **ffmpeg_options)) 
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
