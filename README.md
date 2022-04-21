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
Telegram Application Credentials:<br>
Once the script is executed for the first time, it will create 'config.json'. In this file, you must specify the details of the Telegram application you created.

Channel IDs:<br>
After entering the correct credentials, the script must be executed a second time to create 'channels.json'. This file will contain the names and IDs of the channels separated by a delimiter. The name is irrelevant, but the channel's ID must be valid.

To get the IDs of the Telegram channels you can run 'get_channels.py' which was designed as a standalone program just for this purpose. This program will list all of the channels along with their names and IDs.

Discord Webhooks:<br>
The script must be executed for a third time in order to create 'webhooks.json', which will be required to specify the Discord channel webhooks.

After the previous steps, a Discord Webhook must created. The article below contains information regarding the creation of a webhook.<br>
Discord Webhook Creation - https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks<br>

After the webhook has been created, proceed to specify the name and link in the 'webhooks.json' file.

<b>Video Tutorial:</b><br>
Coming soon...

<b>Recently Added:<b><br>
- Addition of multiple Discord webhooks to send messages to more than one channel.
- Creation of all '.json' files after first execution.

<b>Coming Features:</b><br>
- Check to see if Telegram client successfully connected or exit session.

<b>Bugs/Issues</b><br>
If any issues are found it would be appreciated if they are reported, thank you.<br>
