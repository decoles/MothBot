import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import random
import os
from dotenv import load_dotenv
from time import sleep

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

# @bot.command()
# async def join(ctx):
#     #if user who is running command in voice channel then it will run the following command else do soemthing else
#     if(ctx.author.voice):
#         channel = ctx.message.author.voice.channel
#         voice = await channel.connect()
#         source = FFmpegPCMAudio('./sounds/crusher.wav')
#         player = voice.play(source)
#     else:
#         await ctx.send("NOT IN VOICE CHANNEL YA BUM")

# @bot.command()
# async def leave(ctx):
#     if(ctx.voice_client):
#         await ctx.guild.voice_client.disconnect() #Go to server then go to voice client and remove it
#         await ctx.send("Voice channel lef")
#     else:
#         await ctx.send("Not in voice channel")

#enables custom help command
bot.remove_command("help")
@bot.command()
async def help(ctx):
    await ctx.send("Commands are ```sound```")


@bot.command()
async def sound(ctx):
    if(ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('./sounds/crusher.wav')
        player = voice.play(source)    
        while voice.is_playing():
            continue
        await ctx.guild.voice_client.disconnect() #Go to server then go to voice client and remove it


bot.run(TOKEN)