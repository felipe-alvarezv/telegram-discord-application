import json
from telethon import TelegramClient

def load_configuration_file():
    # Load the configuration for the Telegram API
    try:
        config = open('config.json')
        telegram_data = json.load(config)
        config.close()
        phone_number = telegram_data['phone_number']
        api_id = telegram_data['api_id']
        api_hash = telegram_data['api_hash']

        # Check if default settings were changed
        if phone_number != "CHANGEME" and api_id != "CHANGEME" and api_hash != "CHANGEME":
            # Initialization of TelegramClient
            return TelegramClient(phone_number, api_id, api_hash)
        else:
            print("[TDA] ERROR: The default values in 'config.json' must be changed.")
            exit()
    # If the configuration file is not found, create a new one with default values
    except FileNotFoundError:
        config = {
            "phone_number": "CHANGEME",
            "api_id": "CHANGEME",
            "api_hash": "CHANGEME"
        }
        with open('config.json', 'w') as outfile:
            json.dump(config, outfile)
        print("[TDA] ERROR: 'config.json' was not found, a new file has been created.")

def load_channels_file():
    # Load the Telegram channels from file
    try:
        all_channels = open('channels.json')
        channel_data = json.load(all_channels)
        all_channels.close()
        channel_list = []
        for channel in channel_data:
            # Check if default settings were changed
            if channel['telegram_id'] != "CHANGEME":
                channel_list.append(int(channel['telegram_id']))
            else:
                print("[TDA] ERROR: The default values in 'channels.json' must be changed.")
                exit()

        return channel_list

    # If file with channels not found create a new one
    except FileNotFoundError:
        channel_list = [{
            "name": "CHANGEME",
            "telegram_id": "CHANGEME"
        }]
        with open('channels.json', 'w') as outfile:
            json.dump(channel_list, outfile)
        print("[TDA] ERROR: 'channels.json' was not found, a new file has been created.")

def load_webhooks_file():
    # Load the configuration file with the specified Discord webhooks
    try:
        all_webhooks = open('webhooks.json')
        webhook_data = json.load(all_webhooks)
        all_webhooks.close()
        webhook_list = []
        for webhook in webhook_data:
            # Check if default settings were changed
            if webhook['webhook_url'] != "CHANGEME":
                webhook_list.append(webhook['webhook_url'])
            else:
                print("[TDA] ERROR: The default values in 'webhooks.json' must be changed.")
                exit()

        return webhook_list

    # If file with webhooks not found create a new one
    except FileNotFoundError:
        webhook_list = [{
            "webhook_name": "CHANGEME",
            "webhook_url": "CHANGEME"
        }]
        with open('webhooks.json', 'w') as outfile:
            json.dump(webhook_list, outfile)
        print("[TDA] ERROR: 'webhooks.json' was not found, a new file has been created.")
