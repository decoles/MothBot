import sqlite3
import discord
from datetime import datetime
from datetime import date

#creates all the tables and database iuf it dosent exist
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
    cur.execute('''
        CREATE TABLE IF NOT EXISTS userLevel (
            userId integer PRIMARY KEY NOT NULL,
            userName text NOT NULL,
            guildId integer NOT NULL,
            xp integer NOT NULL)
    ''')
    #give all users in every server 0 xp
    
    for guild in bot.guilds:
        for member in guild.members:
            try: # if the user is already in the database, it will throw an error
                cur.execute('''INSERT INTO userLevel (userId, userName, guildId, xp) VALUES (?,?,?,?)''' , (member.id, member.name, guild.id, 0))
            except:
                #do nothing
                pass
    try:
        cur.execute('''INSERT INTO guilds (guildId, guildName) VALUES (?,?)''' , (bot.guilds[0].id, bot.guilds[0].name))
        #TODO: add logging here
    except:
        #print(bot.guilds[0].name + " already exists in the database")
        pass
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

async def modifyUserLevel(userId,xp):
    con = sqlite3.connect('mothbot.db')#creates a database file if it doesn't exist, connects to it if it does
    cur = con.cursor() #lets us execute commands
    #check if userxp is 0
    cur.execute('''SELECT xp FROM userLevel WHERE userId = ?''', (userId,))
    retrievedXp = cur.fetchone()[0] + xp
    #verif that xp is not negative
    if retrievedXp < 0:
        retrievedXp = 0
    else:
        retrievedXp = retrievedXp + xp
    cur.execute('''UPDATE userLevel SET xp = ? WHERE userId = ?''', (retrievedXp, userId))
    con.commit()
    con.close()