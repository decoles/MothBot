import discord
import dotenv
from discord.ext import commands
import random
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

#intents are like permissions, required as of 2022
intents = discord.Intents.default()
intents.members = True
intents.messages = True

bot = commands.Bot(command_prefix='?', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

#bot status
# @bot.event
# async def on_ready():
#   activity = discord.Game(name="with a lamp")
#   await bot.change_presence(status=discord.Status.online, activity=activity)

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



bot.run(TOKEN)