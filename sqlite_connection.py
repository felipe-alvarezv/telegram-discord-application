import sqlite3

# Function to load channels from database
def load_channel():
    channels = []
    conn = sqlite3.connect('./channels.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS channels (desc TEXT, id TEXT, webhook TEXT)''')
    result = cur.execute('''SELECT desc FROM channels''')

    for row in result:
        channels.append(row)

    conn.close()
    return channels

#Function to load a channel's information from database
def load_channel_info(desc, option):
    conn = sqlite3.connect('./channels.db') 
    cur = conn.cursor()

    match option:
        case 'id':
            cur.execute('''SELECT id FROM channels WHERE desc = ?''', [desc])
            result = cur.fetchone()
            conn.close()
            return result
        case 'webhook':
            cur.execute('''SELECT webhook FROM channels WHERE desc = ?''', [desc])
            result = cur.fetchone()
            conn.close()
            return result

#Function to add a channel and its information to database
def add_channel(desc, id, webhook):
    conn = sqlite3.connect('./channels.db')
    cur = conn.cursor()
    cur.execute('''INSERT INTO channels (desc, id, webhook) VALUES (?, ?, ?)''', [desc, id, webhook])
    conn.commit()
    conn.close()
    
#Function to delete a channel from database
def delete_channel(desc):
    conn = sqlite3.connect('./channels.db')
    cur = conn.cursor()
    cur.execute('''DELETE FROM channels WHERE desc = ?''', [desc])
    conn.commit()
    conn.close()