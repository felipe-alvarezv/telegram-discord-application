# telegram-to-discord-application
An application with a simple interface that allows Telegram messages from specified channels to be sent to a specified Discord webhook.

<b>Requirements</b><br>
The application uses many libraries, but the only external ones are found below:

Python Libraries:<br>
Tkinter - https://pypi.org/project/tkinter-page/<br>
Discord Webhook - https://pypi.org/project/discord-webhook/<br>
Telethon - https://pypi.org/project/Telethon/<br>

To connect to Telegram, you must acquire API credentials from the link found bellow:

Telegram API Information:<br>
https://core.telegram.org/api/obtaining_api_id

<b>How does it work?</b><br>
The application uses Tkinter to create a user interface that can be navigated with ease. The connection to Telegram is established through the use of Telethon, while the webhook payload is delivered with the Discord Webhook library.

<b>Note:</b> As of right now this application only supports text messages, media is a work in progress.

<b>How to configure it?</b><br>
Once you start the application, navigate to the 'API Credentials' window. Once the correct credentials are provided, a session can be initiated allowing the rest of the program to become accessible. Keep in mind, at least one channel must be added in order to start listening to Telegram messages.

<b>Video Tutorial:</b><br>
Coming soon...

<b>Recently Added:<b><br>
- Complete rework of old abandoned program.
- Addition of user interface with separate tabs and windows.
- Ability to configure API credentials within the program.
- Ability to specify one channel to one webhook.
- SQLite storage for channel information.
- Add or remove channels with ease.
- View added channel's information by clicking on Treeview.
- Much more!

<b>Coming Features:</b><br>
- Ability to translate message before delivering to Discord
- Ability to send media to Discord

<b>Bugs/Issues</b><br>
If any issues are found it would be appreciated if they are reported, thank you.<br>