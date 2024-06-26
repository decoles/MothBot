import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord.ext import tasks
import os
from dotenv import load_dotenv
import asyncio
import commands.botCommands as botCommands #commands.py
import userResponse #userResponses.py
import stats.trackstats as trackstats #trackstats.py
import sqlite3
import commands.videoAudio as videoAudio #videoAudio.py

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
    isSoundExist = os.path.exists("sounds")
    await trackstats.initialize(bot)#initialize database if it dosent exist and create tables

    if not isSoundExist: #if sounds folder doesn't exist, create it
        os.mkdir("sounds")
    recordUserStatus.start()
    

@bot.event
async def on_message(message):
    if message.author == bot.user: #if the message is from the bot itself, ignore it
        return
    await userResponse.ReadMessage(message, bot)
    await trackstats.readMessages(message, bot)

@tasks.loop(seconds=60)
async def recordUserStatus():
    await trackstats.recordUserStatus(bot)

@bot.command()
async def stop(ctx):
    await videoAudio.stop(ctx, bot)

#enables custom help command
bot.remove_command("help")
@bot.command()
async def help(ctx):
    await botCommands.help(ctx)

@bot.command() #plays sound or youtube link
async def play(ctx, *, prompt: str = None, bot = bot):
    if(prompt == None):
        await ctx.send("Please enter a youtube link")
        return
    await videoAudio.play(ctx, prompt=prompt, bot=bot)

@bot.command() 
async def queue(ctx):
    await videoAudio.viewQueue(ctx)

@bot.command() 
async def skip(ctx):
    await videoAudio.skip(ctx, bot)

@bot.command()
async def pause(ctx):
    await videoAudio.pause(ctx, bot)

@bot.command()
async def resume(ctx):
    await videoAudio.resume(ctx, bot)

@bot.command() #detects a given link TODO: allow for image uploads
async def detect(ctx, *arg):
    await detection.detect(ctx, *arg)

@bot.command() #pings given servers
async def ping(ctx):
    await botCommands.ping(ctx, bot)

@bot.command()
async def mock(ctx):
    await botCommands.mock(ctx)

@bot.command()
async def generate(ctx, *, prompt: str = None):
    if(prompt == None):
        await ctx.send("Please enter a prompt")
        return
    await botCommands.generate(ctx, prompt=prompt)

@bot.command()
async def games(ctx, *arg):
    await botCommands.games(ctx, bot, *arg)

@bot.command()
async def button(ctx):
    view = discord.ui.View()
    button = discord.ui.Button(label="Click me!", style=discord.ButtonStyle.green)
    view.add_item(button)
    await ctx.send(view=view)
bot.run(TOKEN)