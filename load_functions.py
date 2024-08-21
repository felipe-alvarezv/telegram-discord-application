import os
import json
import pickle

# Function to load channel along with their information (desc, id, webhook)
def load_channel():
    try:
        directory = './channels/'
        channels = []
        
        for file in os.listdir(directory):
            if file.endswith('.pkl'):
                with open(directory + file, 'rb') as f:
                    temp_channel = pickle.load(f)
                    channels.append(temp_channel)
        return channels
    except FileNotFoundError:
        print("[TDA] ERROR: No channel files found")

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

#Function to load channel and store as list
def load_channel_list():
    channels = [] #Empty list to store channels
    directory = './channels/' #Path to channel directory

    for file in os.listdir(directory): #Search for files in specified directory
        if file.endswith('.pkl'): #Match files that end with '.pkl'
            with open(directory + file, 'rb') as f:
                temp_channel = pickle.load(f)
                channels.append([temp_channel.get_desc(), temp_channel.get_id(), temp_channel.get_webhook()])

    return channels #Return a list containing channels