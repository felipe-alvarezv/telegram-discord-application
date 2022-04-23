# telegram-to-discord-application
An application which sends messages from Telegram to Discord.

<b>Requirements</b><br>
This application requires Telethon and Discord Webhook. You must also create a Telegram application on their website.

Python Libraries:<br>
Telethon - https://pypi.org/project/Telethon/<br>
Discord Webhook - https://pypi.org/project/discord-webhook/

Telegram Application Information:<br>
https://core.telegram.org/api/obtaining_api_id

<b>How does it work?</b><br>
This application uses Telethon to fetch the messages being sent on the Telegram channels specified in the configuration file, afterwards sending them to the specified Discord channel webhook. The Telegram application settings and channels, along with the Discord channel webhooks can be configured in the files which will be created after the program's execution.<br>

<b>Note:</b> As of right now this application only supports text messages, soon I will work on media such as images and videos.

<b>How to configure it?</b><br>
First, the script must be executed in order to create all the necessary configuration files. These files will include 'config.json', 'channels.json' and 'webhooks.json'. These files must be altered and configured correctly for this application to work as intended.

Telegram Application Credentials:<br>
After the creation of 'config.json', you must specify the details of Telegram application that are provided on their website in this file.

Channel IDs:<br>
The 'channels.json' file will contain the information of the Telegram channels that you want to get the messages from. In this file you will need to specify their name and ID.

<b>Note:</b> The channel ID must be valid or no messages will be detected.

To get the IDs of the Telegram channels you can run 'get_channels.py' which was designed as a standalone program just for this purpose. This program will list all of the channels along with their names and IDs.

Discord Webhooks:<br>
The 'webhooks.json' file will contain all the Discord webhooks which will be used to send the messages. The article below contains information regarding the creation of a webhook.<br>
Discord Webhook Creation - https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks<br>

After the webhook has been created, proceed to specify the name and URL in the 'webhooks.json' file.

<b>Video Tutorial:</b><br>
Coming soon...

<b>Recently Added:<b><br>
- Addition of multiple Discord webhooks to send messages to more than one channel.
- Creation of all '.json' files after first execution.

<b>Coming Features:</b><br>
- Potential convertion from JSON to SQLite.
- Choose a channel to send a message to specific webhook.
- Check to see if Telegram client successfully connected or exit session.

<b>Bugs/Issues</b><br>
If any issues are found it would be appreciated if they are reported, thank you.<br>
