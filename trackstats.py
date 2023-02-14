import sqlite3
import discord
from datetime import datetime
from datetime import date

async def initialize(bot):
    con = sqlite3.connect('mothbot.db')#creates a database file if it doesn't exist, connects to it if it does
    cur = con.cursor() #lets us execute commands
    cur.execute('''
        CREATE TABLE IF NOT EXISTS guilds (
            guildId integer PRIMARY KEY AUTOINCREMENT NOT NULL, 
            guildName text NOT NULL)
    ''')
    #table for message stats
    cur.execute('''
        CREATE TABLE IF NOT EXISTS messageStats (
            messageId integer PRIMARY KEY NOT NULL, 
            date text NOT NULL, time text NOT NULL, 
            guildId integer NOT NULL, 
            channelId integer NOT NULL, 
            channelName text NOT NULL, 
            authorId integer NOT NULL, 
            authorName text NOT NULL, 
            message text)
    ''')
    #table for user stats
    cur.execute('''
        CREATE TABLE IF NOT EXISTS userStats (
            statId integer PRIMARY KEY AUTOINCREMENT NOT NULL,
            userId integer NOT NULL,
            userName text NOT NULL,
            guildId integer NOT NULL,
            currentStatus text NOT NULL,
            currentActivity text NOT NULL)
    ''')
    try:
        cur.execute('''INSERT INTO guilds (guildId, guildName) VALUES (?,?)''' , (bot.guilds[0].id, bot.guilds[0].name))
    except:
        print("Guild already exists")
    con.commit()
    con.close()

async def readMessages(message, bot):
    #get only current date
    today = date.today()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    con = sqlite3.connect('mothbot.db')#creates a database file if it doesn't exist, connects to it if it does

    cur = con.cursor() #lets us execute commands
    cur.execute('''INSERT INTO messageStats (messageId, date, time, guildId, channelId, channelName, authorId, authorName, message) VALUES (?,?,?,?,?,?,?,?,?)''' ,
     (message.id ,today, current_time, message.guild.id, message.channel.id, message.channel.name, message.author.id, message.author.name, message.content))

    con.commit()

    for row in cur.execute('''SELECT * FROM guilds'''):
        print(row)
    for row in cur.execute('''SELECT * FROM messageStats'''):
        print(row)

    con.close()

#gets all users in the server and records their status i.e online, offline, idle, dnd
async def recordUserStatus(bot):
    con = sqlite3.connect('mothbot.db')#creates a database file if it doesn't exist, connects to it if it does
    cur = con.cursor() #lets us execute commands
    for guild in bot.guilds:
        for member in guild.members:
            cur.execute('''INSERT INTO userStats (userId, userName, guildId, currentStatus, currentActivity) VALUES (?,?,?,?,?)''' , (member.id, member.name, guild.id, str(member.status), str(member.activity)))
    con.commit()
    con.close()