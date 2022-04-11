import json
from telethon import TelegramClient, events
from discord_webhook import DiscordWebhook


def main():
    # Load configuration files for settings
    telegram_client, discord_webhook = load_configuration_file()
    channel_list = load_channels_file()

    # Send a message to console about bot status
    print("[TelegramBot] The bot has been initialized.")

    get_telegram_message(telegram_client, channel_list, discord_webhook)

    # Start the TelegramClient and run on loop
    telegram_client.start()
    telegram_client.run_until_disconnected()


def load_configuration_file():
    # Load the configuration for the Telegram API
    try:
        config = open('config.json')
        telegram_data = json.load(config)
        config.close()
        phone_number = telegram_data['phone_number']
        api_id = telegram_data['api_id']
        api_hash = telegram_data['api_hash']
        discord_webhook = telegram_data['discord_webhook']

        # Check if default settings were changed
        if phone_number != "CHANGEME" and api_id != "CHANGEME" and api_hash != "CHANGEME" and discord_webhook != "CHANGEME":
            # Initialization of TelegramClient
            return TelegramClient(phone_number, api_id, api_hash), discord_webhook
        else:
            print("[ERROR] The default values in 'config.json' must be changed.")
            exit()
    # If the configuration file is not found, create a new one with default values
    except FileNotFoundError:
        config = {
            "phone_number": "CHANGEME",
            "api_id": "CHANGEME",
            "api_hash": "CHANGEME",
            "discord_webhook": "CHANGEME"
        }
        with open('config.json', 'w') as outfile:
            json.dump(config, outfile)
        print("[ERROR] 'config.json' was not found, a new file has been created. Please re-start the program.")
        exit()


def load_channels_file():
    # Load the Telegram channels from file
    try:
        all_channels = open('channels.json')
        channels_data = json.load(all_channels)
        all_channels.close()
        channels_list = []
        for channel in channels_data:
            # Check if default settings were changed
            if channel['telegram_id'] != "CHANGEME":
                channels_list.append(channel['telegram_id'])
            else:
                print("[ERROR] The default values in 'channels.json' must be changed.")
                exit()

        return channels_list

    # If file with channels not found create a new one
    except FileNotFoundError:
        channel_list = [{
            "name": "CHANGEME",
            "telegram_id": "CHANGEME"
        }]
        with open('channels.json', 'w') as outfile:
            json.dump(channel_list, outfile)
        print("[ERROR] 'channels.json' was not found, a new file has been created. Please re-start the program.")
        exit()


def get_telegram_message(telegram_client, channels_list, discord_webhook):
    # Telegram Event Handler - NewMessage
    @telegram_client.on(events.NewMessage([channels_list]))
    async def telegram_message_received(event):
        # Send a message to console about a new message
        sender = await event.get_sender()
        print("[Telegram Message] Time: ", event.date.strftime("%m/%d/%Y, %H:%M:%S"), "\tBy: ", sender.username)

        # If the message contains text
        if event.text:
            # Send text message to DiscordWebhook
            message = event.text
            webhook = DiscordWebhook(url=discord_webhook, content=message)
            response = webhook.execute()


if __name__ == '__main__':
    main()