from load_configurations import load_configuration_file, load_channels_file, load_webhooks_file
from telethon import events
from discord_webhook import DiscordWebhook


def main():
    # Load configuration files for settings
    telegram_client = load_configuration_file()
    channel_list = load_channels_file()
    webhook_list = load_webhooks_file()

    # Send a message to console about bot status
    print("[TDA] The application has been initialized.")

    get_telegram_message(telegram_client, channel_list, webhook_list)

    # Start the TelegramClient and run on loop
    telegram_client.start()
    telegram_client.run_until_disconnected()

def get_telegram_message(telegram_client, channel_list, webhook_list):
    # Telegram Event Handler - NewMessage
    @telegram_client.on(events.NewMessage(chats=channel_list))
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
            for webhook in webhook_list:
                webhook_payload = DiscordWebhook(url=webhook, content=message)
                response = webhook_payload.execute()


if __name__ == '__main__':
    main()
