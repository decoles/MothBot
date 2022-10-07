# bot.py
import os
import random

import discord
from dotenv import load_dotenv
from discord.ext import tasks
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

client = discord.Client()

print(TOKEN)
@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

#bot status
@client.event
async def on_ready():
  activity = discord.Game(name="with a lamp")
  await client.change_presence(status=discord.Status.online, activity=activity)

#prviate message to new members
@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )


bot = commands.Bot(command_prefix="$")
@bot.command()
async def ping(ctx):
	await ctx.channel.send("pong")
async def stats(ctx):
    await ctx.channel.send("pong")


@client.event
async def on_message(message):
    if message.author == client.user: #if the message is from the bot itself, ignore it
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