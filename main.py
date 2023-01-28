import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import random
import os
from dotenv import load_dotenv
import asyncio


load_dotenv()

TOKEN = os.getenv("TOKEN")
#ctx allows communications and properties
#intents are like permissions, required as of 2022

bot = commands.Bot(command_prefix='.', intents=discord.Intents.all()) #use all features

@bot.event
async def on_ready():
    activity = discord.Game(name="with a lamp")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.event
async def on_message(message):
    if message.author == bot.user: #if the message is from the bot itself, ignore it
        return
    light = [
        'GIVE LAMP!',
        'SMOTHER ME WITH LIGHT BULB!',
    ]

    if "kyle" in message.content.lower():
        await message.channel.send("SHUDUP BRIAN")

    if "light" in message.content:
        response = random.choice(light)
        await message.channel.send(response)  
    await bot.process_commands(message)

@bot.command()
async def stop(ctx):
    voice = None
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.stop()
    else:
        await ctx.send("Nothing is playing")
    await ctx.guild.voice_client.disconnect() #Go to server then go to voice client and remove it
    

def soundList():
    sounds = []
    for file in os.listdir("./sounds"):
        sounds.append(file)
    return sounds

#enables custom help command
bot.remove_command("help")
@bot.command()
async def help(ctx):
    await ctx.send("```sounds:\n .sounds - list all sounds\n .play <sound> - play sound\n .stop - stop playing sound\n\nother:\n .help - list all commands\n .ping - pong!```")

@bot.command()
async def sounds(ctx):
    await ctx.send("```Sounds:\n " + "\n ".join(soundList()) + "```")

@bot.command()
async def play(ctx, *arg):
    if arg.__len__() == 0:
        await ctx.send("Please specify a sound")
        return
    elif arg[0] not in soundList():
        await ctx.send("Sound not found")
        return
    voice = None
    player = None
    if(ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        #source = FFmpegPCMAudio('./sounds/nut.mp3')
        source = FFmpegPCMAudio('./sounds/' + arg[0])
        player = voice.play(source)    
        while voice.is_playing():
            await asyncio.sleep(1) #wait for sound to finish
        await ctx.guild.voice_client.disconnect() #Go to server then go to voice client and remove it
    else:
        await ctx.send("Not in voice channel")


bot.run(TOKEN)