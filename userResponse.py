import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import random
import os
from dotenv import load_dotenv
import asyncio
import commands.botCommands as botCommands #commands.py
import commands.detection as detection #detection.py
import userResponse #userResponses.py

async def ReadMessage(message, bot):
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