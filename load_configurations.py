import pickle
import json

# Function to load configuration for Telegram client
def load_configuration():
    try:
        config_file = open('config.json')
        config_data = json.load(config_file)
        config_file.close()
        return config_data

    except FileNotFoundError:
        config_file = {
            "api_id": "CHANGEME",
            "api_hash": "CHANGEME",
            "app_title": "CHANGEME"
        }
        with open('config.json', 'w') as outfile:
            json.dump(config_file, outfile, indent=4)
        print("[TDA] ERROR: 'config.json' was not found, a new file has been created.")

# Function to load channels along with their information (name, id, wehooks)
def load_channels():
    try:
        channels_list = []
        channels_file = open('./channels.pkl', 'rb')
        channels_data = pickle.load(channels_file)
        channels_file.close()
        channels_list.append(channels_data)
        return channels_list
    except FileNotFoundError:
        print("[TDA] ERROR: 'channels.pkl' was not found, make sure to add at least one channel.")
