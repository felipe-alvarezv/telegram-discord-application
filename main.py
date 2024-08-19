import os
import json
import pickle
from telethon import events, TelegramClient
from discord_webhook import DiscordWebhook
import tkinter as tk
from Channel import Channel
from load_configuration import load_configuration
from load_channel import load_channel

def initialize():
    # Load configuration files for settings
    config_data = load_configuration()

    # Check if the Telegram credentials were changed
    if config_data['api_id'] != "CHANGEME" and config_data['api_hash'] != "CHANGEME" and config_data['app_title'] != "CHANGEME":
        telegram_client = TelegramClient(config_data['app_title'], config_data['api_id'], config_data['api_hash'])

    if telegram_client:
        # Start the TelegramClient and return it
        return telegram_client.start()
    else:
        print("[TDA] ERROR: The credentials found in 'config.json' are incorrect.")
        exit()

#Main Page
def main_page_click(root, frame, telegram_client):    
    frame.destroy()
    frame = tk.Frame(root)
    frame.grid(row=0, column=0)

    #Align buttons in the center
    frame.columnconfigure(0, weight=1)

    info_btn = tk.Button(frame, text="Information", width=20, command=lambda: info_btn_click(root, frame, telegram_client))
    info_btn.grid(row=0, column=0)

    channel_btn = tk.Button(frame, text="Channel Management", width=20, command=lambda: channel_btn_click(root, frame, telegram_client))
    channel_btn.grid(row=1, column=0)

    application_btn = tk.Button(frame, text="Start Application", width=20, command=lambda: application_btn_click(root, frame, telegram_client))
    application_btn.grid(row=2, column=0)

#Information Page
def info_btn_click(root, frame, telegram_client):
    frame.destroy()
    frame = tk.Frame(root)
    frame.grid(row=0, column=0)

    info_label = tk.Label(frame, text="The purpose of this application is to foward messages from a Telegram channel to a Discord webhook.\nMedia is not currently supported.")
    info_label.grid(row=0, column=0)
    
    author_label = tk.Label(frame, text="Made by Felipe Alvarez")
    author_label.grid(row=1, column=0)

    return_button = tk.Button(frame, text="Main Page", command=lambda: main_page_click(root, frame, telegram_client))
    return_button.grid(row=2, column=0)

#Channel Management Page
def channel_btn_click(root, frame, telegram_client):
    frame.destroy()
    frame = tk.Frame(root)
    frame.grid(row=0, column=0)

    directory = './channels/'
    channels = []
    
    for file in os.listdir(directory):
        if file.endswith('.pkl'):
            with open(directory + file, 'rb') as f:
                temp_channel = pickle.load(f)
                channels.append([temp_channel.get_desc(), temp_channel.get_id(), temp_channel.get_webhook()])
    
    #Create listbox and add all existing channel files
    channel_list = tk.Listbox(frame, width=50)
    channel_list.grid(row=0, column=0)

    for channel in channels:
        channel_list.insert("end", channel)

    channel_add = tk.Button(frame, text="+", command=lambda: channel_add_click(root, frame, telegram_client))
    channel_add.grid(row=0, column=1)

    channel_modify = tk.Button(frame, text="M", command=lambda: channel_modify_click(root, frame, channel_list, telegram_client))
    channel_modify.grid(row=0, column=2)

    channel_delete = tk.Button(frame, text="-", command=lambda: channel_delete_click(root, frame, channel_list, telegram_client))
    channel_delete.grid(row=0, column=3)

    return_button = tk.Button(frame, text="Main Page", command=lambda: main_page_click(root, frame, telegram_client))
    return_button.grid(row=1, column=0)

#Application Page
def application_btn_click(root, frame, telegram_client):
    frame.destroy()
    frame = tk.Frame(root)
    frame.grid(row=0, column=0)

    root.destroy()
    listen(telegram_client)

#Add Channel Page
def channel_add_click(root, frame, telegram_client):
    frame.destroy()
    frame = tk.Frame(root)
    frame.grid(row=0, column=0)

    #Varianble to store existing channels
    channels = []
    for dialog in telegram_client.iter_dialogs():
        if dialog.is_channel:
            temp_channel = [dialog.title, dialog.id * -1]
            channels.append(temp_channel)

    #Variable to store selected channel
    selected_channel = tk.Variable(frame)

    description_label = tk.Label(frame, text="Description:")
    description_label.grid(row=0, column=0)

    description_entry = tk.Entry(frame)
    description_entry.grid(row=0, column=1)

    channel_label = tk.Label(frame, text="Channel:")
    channel_label.grid(row=1, column=0)

    channel_id = tk.OptionMenu(frame, selected_channel, *channels)
    channel_id.grid(row=1, column=1)

    discord_label = tk.Label(frame, text="Discord Webhook:")
    discord_label.grid(row=2, column=0)

    discord_webhook = tk.Entry(frame)
    discord_webhook.grid(row=2, column=1)

    add_channel_btn = tk.Button(frame, text="Add Channel", command=lambda: add_channel_btn_clicked(root, frame, description_entry, selected_channel, discord_webhook, telegram_client))
    add_channel_btn.grid(row=3, column=0)

    discard_channel_btn = tk.Button(frame, text="Discard", command=lambda: channel_btn_click(root, frame, telegram_client))
    discard_channel_btn.grid(row=3, column=1)

#Add Channel Button Event
def add_channel_btn_clicked(root, frame, description_entry, selected_channel, discord_webhook, telegram_client):
    if description_entry.get() and selected_channel and discord_webhook.get():
        filename = 'channels/' + description_entry.get() + '.pkl'
        channel_file = open(filename, 'wb')
        temp_channel = Channel(description_entry.get(), selected_channel.get()[1], discord_webhook.get()) #Make a Channel object with the passed variable
        pickle.dump(temp_channel, channel_file)
        channel_file.close()

        frame.destroy()
        channel_btn_click(root, frame, telegram_client)
    else:
        frame.destroy()
        channel_add_click(root, frame, telegram_client)

#Modify Channel Page
def channel_modify_click(root, frame, channel_list, telegram_client):
    #Variable to store channel object
    channel = []

    for i in channel_list.curselection():
        channel = channel_list.get(i)

    frame.destroy()
    frame = tk.Frame(root)
    frame.grid(row=0, column=0)

    if channel:
        description_label = tk.Label(frame, text="Description:")
        description_label.grid(row=1, column=0)

        description_entry = tk.Entry(frame)
        description_entry.grid(row=1, column=1)
        description_entry.insert("end", channel[0])

        discord_label = tk.Label(frame, text="Discord Webhook:")
        discord_label.grid(row=2, column=0)

        discord_webhook = tk.Entry(frame)
        discord_webhook.grid(row=2, column=1)
        discord_webhook.insert("end", channel[2])

        save_channel_btn = tk.Button(frame, text="Save", command=lambda: save_channel_btn_clicked(root, frame, channel, description_entry, discord_webhook, telegram_client))
        save_channel_btn.grid(row=3, column =0)

        discard_channel_btn = tk.Button(frame, text="Discard", command=lambda: channel_btn_click(root, frame, telegram_client))
        discard_channel_btn.grid(row=3, column=1)

#Save Modified Channel Event
def save_channel_btn_clicked(root, frame, channel, description_entry, discord_webhook, telegram_client):
    if description_entry and discord_webhook:
        channel_description = description_entry.get()

        original_filename = 'channels/' + channel[0] + '.pkl'
        filename = 'channels/' + channel_description + '.pkl'
        channel_file = open(filename, 'wb')

        os.remove(original_filename) #Delete original channel files
        temp_channel = Channel(channel_description, channel[1], discord_webhook.get()) #Make a Channel object with the passed variable
        pickle.dump(temp_channel, channel_file)
        channel_file.close()

        frame.destroy()
        channel_btn_click(root, frame, telegram_client)
    else:
        frame.destroy()
        channel_add_click(root, frame, telegram_client)

    frame.destroy()
    channel_btn_click(root, frame, telegram_client)

#Delete Channel Page
def channel_delete_click(root, frame, channel_list, telegram_client):
    #Variable to store channel object
    channel_id = []

    for i in channel_list.curselection():
        channel = channel_list.get(i)

    frame.destroy()
    frame = tk.Frame(root)
    frame.grid(row=0, column=0)

    delete_label = tk.Label(frame, text="Are you sure you want to delete this channel?")
    delete_label.grid(row=0, column=0)

    delete_channel_btn = tk.Button(frame, text="Yes", command=lambda: delete_channel_btn_clicked(root, frame, channel, telegram_client)) 
    delete_channel_btn.grid(row=0, column=1)

    cancel_delete_btn = tk.Button(frame, text="No", command=lambda: channel_btn_click(root, frame, telegram_client))
    cancel_delete_btn.grid(row=0, column=2)

#Delete Channel Event
def delete_channel_btn_clicked(root, frame, channel, telegram_client):
     if channel:
        filename = 'channels/' + channel[0] + '.pkl'
        os.remove(filename) #Delete channel file

        frame.destroy()
        channel_btn_click(root, frame, telegram_client)

def main():
    # Initialize client with config data
    telegram_client = initialize()

    root = tk.Tk()
    root.minsize(250, 125)
    root.maxsize(400, 400)
    root.title("Telegram to Discord App")

    frame = tk.Frame(root)
    frame.grid(row=0, column=0)

    main_page_click(root, frame, telegram_client)
    root.mainloop()

def listen(telegram_client):
    channels_data = load_channel()
    get_telegram_message(telegram_client, channels_data)
    print("[TDA] The application has been started, to exit hold Ctrl + C.")
    telegram_client.run_until_disconnected()


def get_telegram_message(telegram_client, channels_data):
    channel_id_list = []
    for channel in channels_data:
        channel_id_list.append(channel.get_id())

    # Telegram Event Handler - NewMessage
    @telegram_client.on(events.NewMessage(chats=channel_id_list))
    async def telegram_message_received(event):
        # Send a message to console about a new message
        sender = await event.get_sender()

        print("[TDA] ----- A new message has been received. -----")
        print("%-25s %-25s %-25s" % ("Date and Time", "Channel ID", "Author ID"))
        print("%-25s %-25s %-25s" % (event.date.strftime("%m/%d/%Y, %H:%M:%S"), event.peer_id.channel_id, sender.id))

        # If the message contains text
        if event.text:
            # Store the event message
            message = event.text

            #Send message to webhook
            webhook = channel.get_webhook()
            if webhook:
                webhook_payload = DiscordWebhook(url=webhook, content=message)
                response = webhook_payload.execute()

if __name__ == '__main__':
    main()
