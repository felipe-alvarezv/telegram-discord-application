import sqlite3

#Function to create necessary table for channels
def create_tables():
    conn = sqlite3.connect('./channels.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS channels (desc TEXT PRIMARY KEY, id TEXT, webhook TEXT)''')
    conn.commit()
    conn.close()

#Function to load channels from database
def load_channel():
    channels = []
    conn = sqlite3.connect('./channels.db')
    cur = conn.cursor()
    result = cur.execute('''SELECT desc, id, webhook FROM channels''')

    if result:
        for row in result:
            channels.append(row)

    conn.close()
    return channels

#Function to select channel with specified description
def load_channel_by_description(desc):
    conn = sqlite3.connect('./channels.db')
    cur = conn.cursor()
    cur.execute('''SELECT * FROM channels WHERE desc = ?''', [desc])
    result = cur.fetchone()
    conn.close()

    if result:
        return result

#Function to add a channel and its information to database
def add_channel(desc, id, webhook):
    conn = sqlite3.connect('./channels.db')
    cur = conn.cursor()
    try:
        cur.execute('''INSERT INTO channels (desc, id, webhook) VALUES (?, ?, ?)''', [desc, id, webhook])
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

#Function to delete a channel from database
def delete_channel(desc):
    conn = sqlite3.connect('./channels.db')
    cur = conn.cursor()
    cur.execute('''DELETE FROM channels WHERE desc = ?''', [desc])
    conn.commit()
    conn.close()

#Function to check if channels table is populated
def is_channels_populated():
    conn = sqlite3.connect('./channels.db')
    cur = conn.cursor()
    cur.execute('''SELECT EXISTS (SELECT 1 FROM channels)''')
    result = cur.fetchone()
    conn.close()

    if result:
        if result[0] == 1:
            return True