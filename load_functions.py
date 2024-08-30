import os
import json
import sqlite3

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