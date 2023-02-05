import sqlite3

async def dbtest(ctx, bot):

    con = sqlite3.connect('trackstats.db')

    cur = con.cursor() #lets us execute commands

    cur.execute('''CREATE TABLE IF NOT EXISTS stats (guild text, username text, userid text, message text, time text)''')

    cur.execute('''INSERT INTO stats VALUES ('test', 'test', 'test', 'test', 'test')''')

    con.commit()

    for row in cur.execute('''SELECT * FROM stats'''):
        print(row)