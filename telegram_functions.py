from telethon import events, TelegramClient
from discord_webhook import DiscordWebhook
from load_functions import load_configuration, load_channel

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