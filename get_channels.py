from load_configurations import load_configuration_file
from telethon import TelegramClient, events

def main():
    # Load configuration files for settings
    telegram_client = load_configuration_file()

    # Start the TelegramClient and run on loop
    telegram_client.start()

    # Show the channels the user is part of
    print("%-25s %-25s" % ("Channel ID", "Channel Name"))

    for dialog in telegram_client.iter_dialogs():
          if dialog.is_channel:
              print("%-25s %-25s" % (dialog.id, dialog.title))

    exit()

if __name__ == '__main__':
    main()
