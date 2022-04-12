# telegram-discord-integration
An integration that will send messages from selected channels in Telegram to a Discord webhook.

<b>Requirements</b><br>
This application requires Telethon and Discord Webhook. You must also create a Telegram application on their website. 

Python Libraries:<br>
Telethon - https://pypi.org/project/Telethon/<br>
Discord Webhook - https://pypi.org/project/discord-webhook/

Telegram Application Information:<br>
https://core.telegram.org/api/obtaining_api_id

<b>How does it work?</b><br>
This application uses Telethon to fetch the messages being sent on the Telegram channels specified in the configuration file, afterwards sending them to the specified webhook. The Telegram application settings and channels can be configured in the files which will be created after its execution.

<b>How to configure it?</b><br>
Telegram Application Credentials:<br>
Once the script is executed for the first time, it will create 'config.json'. In this file, you must specify the details of the Telegram application you created.

Discord Webhook:<br>
After the previous step, a Discord Webhook must created. The article below contains information regarding the creation of a webhook.<br>
Discord Webhook Creation - https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks<br>

After the webhook has been created, proceed to specify the link in the 'config.json' file.


Channel IDs:<br>
After entering the correct credentials, the script must be executed a second time to create 'channels.json'. This file will contain the names and IDs of the channels separated by a delimeter. The name is irrelevant, but the channel's ID must be valid.

How to get the Telegram channel ID?
