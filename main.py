import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord.ext import tasks
import random
import os
from dotenv import load_dotenv
import asyncio
import botCommands #commands.py
import detection #detection.py
import userResponse #userResponses.py
import trackstats #trackstats.py

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
    isDbExist = os.path.exists("trackstats.db")
    isSoundExist = os.path.exists("sounds")
    if not isSoundExist: #if sounds folder doesn't exist, create it
        os.mkdir("sounds")
    looptest.start()
    

@bot.event
async def on_message(message):
    if message.author == bot.user: #if the message is from the bot itself, ignore it
        return
    await userResponse.ReadMessage(message, bot)

@tasks.loop(seconds=10)
async def looptest():
    print("Changing status")

@bot.command()
async def stop(ctx):
    await botCommands.stop(ctx, bot)

#enables custom help command
bot.remove_command("help")
@bot.command()
async def help(ctx):
    await botCommands.help(ctx)

@bot.command()
async def sounds(ctx):
    await botCommands.sounds(ctx)

@bot.command()
async def play(ctx, *arg):
    await botCommands.play(ctx, *arg)

@bot.command()
async def detect(ctx, arg):
    await detection.detect(ctx, arg)

@bot.command()
async def ping(ctx):
    await botCommands.ping(ctx, bot)

@bot.command()
async def dbtest(ctx):
    await trackstats.dbtest(ctx, bot)

bot.run(TOKEN)