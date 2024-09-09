import json

# Function to load configuration for Telegram connection from JSON file
def load_configuration():
    try:
        config_file = open('config.json')
        config_data = json.load(config_file)
        config_file.close()
        return config_data

    except FileNotFoundError:
        return False

#Function to save configuration for Telegram connection to JSON file
def save_configuration(api_id, api_hash, api_title):
    config_file = {
        'api_id': api_id,
        'api_hash': api_hash,
        'api_title': api_title
    }
    with open('config.json', 'w') as outfile:
        json.dump(config_file, outfile, indent=4)