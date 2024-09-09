from telethon import events, TelegramClient
import telethon.errors.rpcerrorlist as telegram_errors
from discord_webhook import DiscordWebhook
from json_functions import load_configuration
from sqlite_functions import load_channel

#Initializes the Telegram client if API credentials are correct, if not it will return False
def initialize():
    #Load API configuration file
    config_data = load_configuration()

    #Check if API configuration contains any data
    if config_data:
        try:
            telegram_client = TelegramClient(config_data['api_title'], config_data['api_id'], config_data['api_hash']) #Start a Telegram session
            return telegram_client.start()
        except telegram_errors.ApiIdInvalidError: #Exception occurs if invalid API credentials are provided
            return False
    else:
        return False

#Start listening to all of the Telegram client's messages
def listen(telegram_client):
    channels_data = load_channel() #Load all channels from database
    get_telegram_message(telegram_client, channels_data)
    print('[TDA] The application has been started, to exit hold Ctrl + C.')
    telegram_client.run_until_disconnected()

#Gets the Telegram messages of the specified added channels and proceeds to deliver through a Discord webhook
def get_telegram_message(telegram_client, channels_data):
    channel_list = []
    channel_list_id = []
    
    #Load all channels from the database into lists
    for channel in channels_data:
        channel_list.append(channel)
        channel_list_id.append(int(channel[1]))

    #Telegram Event Handler - NewMessage 
    @telegram_client.on(events.NewMessage(chats=channel_list_id))
    async def telegram_message_received(event):
        if event.text:
            message = event.text

            #Iterate through all added channels
            for channel in channel_list:
                channel_id = int(channel[1][3:])

                #Send message to webhook if the channel ID matches any in the list
                if channel_id == event.peer_id.channel_id:
                    webhook = channel[2]
                    if webhook:
                        #Print to console if a message came from an added channel
                        sender = await event.get_sender()
                        print('----------------------------------------------------------------------------------------------------')
                        print('%-25s %-25s %-25s' % ('Date and Time', 'Channel ID', 'Author ID'))
                        print('%-25s %-25s %-25s' % (event.date.strftime('%m/%d/%Y, %H:%M:%S'), event.peer_id.channel_id, sender.id))

                        #Deliver payload to Discord webhook
                        webhook_payload = DiscordWebhook(url=webhook, content=message)
                        webhook_payload.execute()