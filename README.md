## How do I set up this bot for my server?
### Dependencies
To setup this bot for your own use, you will need to install several Python modules listed below assuming you do not already have them.
- pycord
- pytz
- gspread
- oauth2
- python-dotenv

Additionally, create a .env file that contains the variable 'DS_TOKEN' and your bot's token, and a .py file called 'rocketrycfg' that contains an empty string variable with a name of your choosing. The cfg file can be named whatever you'd like, but be sure to change all instances of the name in the code, along with the instances of the variable name.

### Google Sheets Integration
To connect your own Google Sheets info to the bot, you must set up a service account for your own sheet. I recommend finding a guide to tell you how to do this.

Google has their own guide on how to set this up:
https://developers.google.com/sheets/api/quickstart/python

Download the service account credentials .JSON and place it in the bot project directory. Assign the filename to the 'app_json' variable.

You must change the variables 'sh' and 'wks' to match your Sheet name and Worksheet name respectively.

The bot is currently set up to read specific columns in order to verify club dues. Either change your sheet to match these columns, or change the column letter in the code to match your sheet.

### Customization
There are many parts of the code that you will need to change to match your server. These include the guild ID, channel IDs, role IDs, and role names. You can find and replace these in the following functions:
- retrieve_events()
- on_member_join()
- on_message()
- eventMessage()

Every print statement can be changed to match your use case. 
Loop frequency can be changed to update guild scheduled events more or less often.
Pay close attention to the timezone object from pytz to ensure it matches your own timezone.
The variables 'roleUnpaid' and 'roleMember' call roles with the names 'Unpaid Dues' and 'Member'. Ensure your server has roles by these names or that the bot calls the role names of your choosing.

To use the manual reply functionality, your message must be formatted as follows:

\-reply [Target Channel ID]\-[Target Message ID] [Reply Message Content]

E.g. \-reply 991898477112070166\-1027417084273102850 This is a test
