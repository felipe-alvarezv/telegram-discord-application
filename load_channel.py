import os
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
