from load_configurations import load_configuration, load_channels
import json
from Channel import Channel
from telethon import events, TelegramClient
from discord_webhook import DiscordWebhook
import os
import tkinter as tk

#Main Page
def main_page_click(root, frame):    
    frame.destroy()
    frame = tk.Frame(root)
    frame.grid(row=0, column=0)

    info_btn = tk.Button(frame, text="Information", command=lambda: info_btn_click(root, frame))
    info_btn.grid(row=0, column=0)

    channel_btn = tk.Button(frame, text="Channel Management", command=lambda: channel_btn_click(root, frame))
    channel_btn.grid(row=0, column=1)

    application_btn = tk.Button(frame, text="Start Application", command=lambda: application_btn_click(root, frame))
    application_btn.grid(row=0, column=2)

#Information Page
def info_btn_click(root, frame):
    frame.destroy()
    frame = tk.Frame(root)
    frame.grid(row=0, column=0)

    info_label = tk.Label(frame, text="The purpose of this application is to foward messages from a Telegram channel to a Discord webhook.\nMedia is not currently supported.")
    info_label.grid(row=0, column=0)
    
    author_label = tk.Label(frame, text="Made by Felipe Alvarez")
    author_label.grid(row=1, column=0)

    return_button = tk.Button(frame, text="Main Page", command=lambda: main_page_click(root, frame))
    return_button.grid(row=2, column=0)

#Channel Management Page
def channel_btn_click(root, frame):
    frame.destroy()
    frame = tk.Frame(root)
    frame.grid(row=0, column=0)

    channel_list = tk.Listbox(frame)
    channel_list.grid(row=0, column=0)

    channel_add = tk.Button(frame, text="+", command=lambda: channel_add_click(root, frame))
    channel_add.grid(row=1, column=1)

    channel_modify = tk.Button(frame, text="M")
    channel_modify.grid(row=1, column=2)

    channel_delete = tk.Button(frame, text="-")
    channel_delete.grid(row=1, column=3)


#Application Page
def application_btn_click(root, frame):
    frame.destroy()
    frame = tk.Frame(root)
    frame.grid(row=0, column=0)

    root.destroy()

    # Initialize client with config data
    telegram_client = initialize()
    listen(telegram_client)

#Add Channel Page
def channel_add_click(root, frame):
    frame.destroy()
    frame = tk.Frame(root)
    frame.grid(row=0, column=0)

    description_label = tk.Label(frame, text="Description:")
    description_label.grid(row=0, column=0)

    description_entry = tk.Entry(frame)
    description_entry.grid(row=0, column=1)

    channel_label = tk.Label(frame, text="Channel:")
    channel_label.grid(row=1, column=0)

    channel_id = tk.OptionMenu(frame, variable="x", value=1)
    channel_id.grid(row=1, column=1)

    discord_label = tk.Label(frame, text="Discord Webhook:")
    discord_label.grid(row=2, column=0)

    discord_webhook = tk.Entry(frame)
    discord_webhook.grid(row=2, column=1)

    



def main():
    root = tk.Tk()
    root.title("Telegram to Discord App")

    frame = tk.Frame(root)
    frame.grid(row=0, column=0)

    main_page_click(root, frame)
    root.mainloop()


    # Initialize client with config data
    #telegram_client = initialize()

    # Show the text menu options for the program
    #show_menu(telegram_client)

# Define all menu options that are available
def show_menu(telegram_client):
    # Clear the screen for Windows and Linux
    #os.system('cls||clear')

    # Send creator message and available options
    #print("Telegram to Discord Application\n- Created by Felipe Alvarez -\n")
    #print("1. Channel Menu\n2. Start Application\n")

    # Ask user for their menu input option
    #main_menu = int(input("Enter a number: "))

    # If the user chose the first option
    #if main_menu == 1:
        # Show menu options regarding specific channels
    #    show_channel_menu(telegram_client)
    # If the user chose the second option
    #elif main_menu == 2:
        # Call function that begins listening to pre-existing channels and their webhooks
    #    listen(telegram_client)

    window = show_main_gui()

    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, "Exit"):
            break
        if event == "1. Channel Management":
            show_channel_window = show_channel_gui()

            while True:
                event, values = show_channel_window.read()
                if event in (sg.WINDOW_CLOSED, "Exit"):
                    break
                if event == "Add":
                    add_channel_window = add_channel_gui()

                    while True:
                        event, values = add_channel_window.read()
                        if event in (sg.WINDOW_CLOSED, "Exit"):
                            break

                        else:
                            sg.popup_error("Working on it")

                else:
                    sg.popup_error("Working on it")

        else:
            sg.popup_error("Working on it")

# Channel options
def show_channel_menu(telegram_client):
    os.system('cls||clear')
    #print("Telegram to Discord Application\n- Channel Menu -\n")
    #print("1. Add Channel\n2. Modify Channel Webhooks\n3. Delete Channel\n4. Back")
    #channel_menu = int(input("Enter a number: "))

    #if channel_menu == 1:
    #    add_channel(telegram_client)
    #elif channel_menu == 2:
    #    print("Second option")
    #elif channel_menu == 3:
    #    print("Third option")
    #elif channel_menu == 4:
    #    print("Fourth option")

def add_channel(telegram_client):
    os.system('cls||clear')
    #channel_list = []

    #for dialog in telegram_client.iter_dialogs():
    #      if dialog.is_channel:
    #          channel_list.append([dialog.id * -1, dialog.title])

    #if channel_list:
    #    print("%-20s %-20s %-20s" % ("Index", "ID", "Title"))
    #    for channel in channel_list:
    #        print("%-20d %-20d %-20s" % (channel_list.index(channel), channel[0], channel[1]))

    #    channel_index = int(input("\nEnter a channel index: "))
    #    if channel_index >= 0 or channel_index < len(channel_list):
    #        webhook = input("Enter a webhook link: ")
    #        channels_file = open('./channels.pkl', 'wb')
    #        channel_object = Channel(channel_list[channel_index][0], channel_list[channel_index][1], webhook)
    #        pickle.dump(channel_object, channels_file)
    #        channels_file.close()
    #    else:
    #        print("Invalid index.")
    #else:
    #    print("You must be in at least one Telegram channel.")

def add_channel_webhooks():
    os.system('cls||clear')
    #print("You ")
    #print("")

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

def listen(telegram_client):
    channels_data = load_channels()
    get_telegram_message(telegram_client, channels_data)
    print("[TDA] The application has been started, to exit hold Ctrl + C.")
    telegram_client.run_until_disconnected()


def get_telegram_message(telegram_client, channels_data):
    for channel in channels_data:
        # Telegram Event Handler - NewMessage
        @telegram_client.on(events.NewMessage(chats=channel.get_id()))
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

                # Iterate through all webhooks and send message
                for webhook in channel.get_channel_webhooks():
                    if webhook:
                        webhook_payload = DiscordWebhook(url=webhook, content=message)
                        response = webhook_payload.execute()

if __name__ == '__main__':
    main()
