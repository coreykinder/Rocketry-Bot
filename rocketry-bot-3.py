import os
import time
import threading
import asyncio
import discord
import gspread
import itertools
from dotenv import load_dotenv
from discord.ext import commands, tasks
from discord import Intents
from oauth2client.service_account import ServiceAccountCredentials
import json
import re
import requests
from datetime import datetime
import pytz
import rocketrycfg

# Get Discord Token & Sheets Service Account
load_dotenv()
DS_TOKEN = os.getenv('DS_TOKEN')

app_json = open('charged-polymer-355300-4fe452072be7.json')
app_creds_dictionary = json.load(app_json)

# Set Discord intents
intents = discord.Intents(
    guilds=True,
    guild_reactions=True,
    scheduled_events=True,
    members=True,
    messages=True,
    message_content=True,
    reactions=True,
)
client = discord.Client(
    intents=intents
)

# Initialize Bot Functions
@client.event
async def on_ready():
    # Set Bot Activity
    activity = discord.Activity(name='with fire', type=discord.ActivityType.playing)
    await client.change_presence(activity=activity)
    # Begin Loops
    eventMessage.start()
    # Log Bot Status at Current Systen Time
    print(time.strftime('%-I:%M:%S %p\nWe have continuity!', time.localtime()))

# Get Discord Server Events with API Request
def retrieve_events():
    # Define Auth
    headers = {
        'Authorization': f"Bot {DS_TOKEN}"
    }
    # Execute Request
    r = requests.get('https://discord.com/api/v9/guilds/972627157513797643/scheduled-events', headers=headers)
    # Assign to Var
    global jsonn
    jsonn = json.loads(r.text)
    # for value in jsonn:
    #     print(value, '\n')

# Get Current System Time in Timezone Aware ISO 8601 Format
def getTime():
    present = datetime.now(pytz.utc)
    now = present.strftime('%Y-%m-%dT%H:%M:%S%z')
    # Insert ':' into Timezone (Ex. '+0400' -> +04:00)
    now = "{0}:{1}".format(
        now[:-2],
        now[-2:]
    )
    return now

def eventsloop():
    while True:
        retrieve_events()
        getTime()
        global databaseWrite
        # Open Database JSON
        with open('rocketrydatabase.json', 'r') as data:
            databaseWrite = json.load(data)
        with open('rocketrydatabase.json', 'r') as f:
            databaseRead = json.load(f)
        # Initialize currentEventsDict Var
        currentEventsDict = {}
        # Build currentEventsDict from retrieve_events Function JSON
        for value in range(len(jsonn)):
            dictID = jsonn[value]['id']
            eventList = {
                dictID:{
                    "name": jsonn[value]['name'],
                    "id": jsonn[value]['id'],
                    "startTime": jsonn[value]['scheduled_start_time'],
                    "endTime": jsonn[value]['scheduled_end_time']
                    }
                }
            uhhhh = eventList[f'{dictID}']
            currentEventsDict[f'{dictID}'] = uhhhh

        # Remove events from JSON cache
        dickweed = [key for key in databaseRead if key not in currentEventsDict]
        for key in dickweed:
            if not dickweed:
                print('No passed events')
            else:
                removeEventName = databaseRead[f'{key}']['name']
                del databaseWrite[f'{key}']
                print(f'Event \'{removeEventName}\' deleted from cache')

        # Add events to JSON cache
        rocketrycfg.weeddick = [key for key in currentEventsDict if key not in databaseRead]
        for key in rocketrycfg.weeddick:
            if not rocketrycfg.weeddick:
                print('No new events')
            else:
                bah = currentEventsDict[key]
                newEventName = currentEventsDict[key]['name']
                databaseWrite[f'{key}'] = bah
                print(f'New event \'{newEventName}\' added to Rocketry Events cache')

        # Write New Events to Database JSON
        with open('rocketrydatabase.json', 'w') as outfile:
            json.dump(databaseWrite, outfile, indent=4)

        time.sleep(3600)

eventLoopThread = threading.Thread(target=eventsloop)
eventLoopThread.start()

# Default Role
roleUnpaid = "Unpaid Dues"
@client.event
async def on_member_join(member):
    roleU = discord.utils.get(member.guild.roles, name=roleUnpaid)
    await member.add_roles(roleU)

# Google Sheets Integration
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_dict(app_creds_dictionary, scope)
sa = gspread.authorize(credentials)
sh = sa.open("Member List 2022-2023")
wks = sh.worksheet("Member List")

# Update Sheets Data
def sheetsLoop():
    counter = 1
    while True:
        global emailsListFlat
        global duesListFlat
        global emailsList

        # Create Flat List from Sheets Emails
        emailsList = wks.get('C2:C150')
        emailsListFlatInit = list(itertools.chain(*emailsList))
        emailsListFlat = [x.lower() for x in emailsListFlatInit]

        # Create Flat List from Sheets Dues
        duesList = wks.get('E2:E150')
        duesListFlatInit = list(itertools.chain(*duesList))
        duesListFlat = [x.lower() for x in duesListFlatInit]

        # Print Sheets Loop Info to Console
        print(time.strftime(f"Rocketry Sheets data last updated %-I:%M:%S %p.\nLoop {counter}\n", time.localtime()))
        counter = counter + 1
        time.sleep(3600)

sheetLoopThread = threading.Thread(target=sheetsLoop)
sheetLoopThread.start()

# Initialize Vars
mixEmail = ''
mixEmailInit = ''
emailIndexInit = ''
roleMember = 'Member'
rowIndex = ''

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Auto Reactions
    if 'cfd' in message.content.lower():
        await message.add_reaction('<:wvuer_cfd:998962804377784321>')

    if 'crack' in message.content.lower() and message.author.id == 415028843280203806:
        await message.add_reaction('<:wvuer_gabeblunt:996862961295564840>')

    if 'balls' in message.content.lower():
        await message.reply('balls')

    # Manual Replies
    try:
        if '-reply' in message.content.lower() and message.channel.id == 993258797365727253:
            # Get Command Message
            commandMessageID = message.id
            commandChannelID = message.channel.id
            # Remove '-reply ' from String
            commandMessage = message.content[7:]
            # Split String into Channel and Message IDs
            msgChnIDs = re.split('[- ]', commandMessage)

            # Assign Channel and Message IDs to Vars
            channelID = int(msgChnIDs[0])
            messageID = int(msgChnIDs[1])
            # Assign Reply Content to Var
            length = len(str(channelID) + '-' + str(messageID) + ' ')
            replyContent = commandMessage[length:]

            # Error if Reply Content Empty
            if replyContent == '':
                channel = client.get_channel(commandChannelID)
                message = await channel.fetch_message(commandMessageID)
                await message.reply('Error in command')
            # Send Reply
            else:
                channel = client.get_channel(channelID)
                message = await channel.fetch_message(messageID)
                await message.reply(replyContent)
    # Catch-All Error Message
    except:
        channel = client.get_channel(commandChannelID)
        message = await channel.fetch_message(commandMessageID)
        await message.reply('Error in command')

    # Dues Verification
    if '@' in message.content and message.channel.id == 992951693874581514:
        # Create Flat List from User Message
        mixEmailInit = [message.content]
        mixEmail = [x.lower() for x in mixEmailInit]

        # Check if User Message is in Sheets Email List
        if [email for email in emailsListFlat if email in mixEmail]:
            # Get Sheets Dues Cell and Verified Cell from Emails List Index
            rowIndex = emailsListFlat.index(mixEmail[0])
            emailIndexInit = emailsList.index(mixEmail)
            emailIndex = emailIndexInit + 2
            verifiedCell = wks.get(f'N{emailIndex}')
            verifiedCell = verifiedCell[0][0]

            # Paid Dues Not Verified
            if duesListFlat[rowIndex] == 'true' and verifiedCell == 'FALSE':
                # Updates roles
                roleM = discord.utils.get(message.author.guild.roles, name=roleMember)
                await message.author.add_roles(roleM)

                roleU = discord.utils.get(message.author.guild.roles, name=roleUnpaid)
                await message.author.remove_roles(roleU)

                # Update 'Joined Discord' and 'Bot Verified' Columns
                wks.batch_update([{
                    'range': f'M{emailIndex}:N{emailIndex}',
                    'values': [['TRUE', 'TRUE']],
                }],
                value_input_option='USER_ENTERED')

                # DM Verified User
                await message.author.send('Thank you for verifying your dues in the WVU Experimental Rocketry server!')

                # Log to Verification Log
                logChannel = client.get_channel(993982483827785798)
                await logChannel.send(f'{message.author.mention} has verified dues.')

            # Paid Dues Already Verified
            elif duesListFlat[rowIndex] == 'true' and verifiedCell == 'TRUE':
                await message.reply(
                    'Our records show this email has already been used to verify dues. If this was not done by you, please contact an admin to resolve the issue.'
                )

            # Unpaid Dues but Somehow Verified
            elif duesListFlat[rowIndex] == 'false' and verifiedCell == 'TRUE':
                wks.batch_update([{
                    'range': f'N{emailIndex}',
                    'values': [['FALSE']],
                }],
                value_input_option='USER_ENTERED')

                # Check if User Has 'Member' Role
                for role in message.author.roles:
                    if str(role) != 'Member':
                        return
                    elif str(role) == 'Member':
                        print('found')
                        # Remove 'Member' Role
                        roleM = discord.utils.get(message.author.guild.roles, name=roleMember)
                        await message.author.remove_roles(roleM)

                        # Add 'Unpaid Dues' Role
                        roleU = discord.utils.get(message.author.guild.roles, name=roleUnpaid)
                        await message.author.add_roles(roleU)
                    else:
                        return

                # Send Unpaid Dues Message to User
                await message.reply(
                    'Unable to verify dues. Our records show you have not paid dues. Contact an admin for assistance if you believe this is a mistake.'
                )

            # Send Unpaid Dues Message to User
            else:
                await message.reply(
                    'Unable to verify dues. Our records show you have not paid dues. Contact an admin for assistance if you believe this is a mistake.'
                )

        # Send Email Not Found Message to User
        elif message.channel.id == 992951693874581514:
            await message.reply(
                'This email does not appear in our records. Please check your message for formatting/spelling errors. Contact an admin for assistance if the problem persists.'
            )

    # Send Improper Format Message to User
    elif message.channel.id == 992951693874581514:
        await message.reply(
            'This does not seem to be a valid email address. Please refer to the verification instructions and check your message for formatting/spelling errors. Contact an admin for assistance if the problem persists.'
        )

# Send new event message
@tasks.loop(seconds=1800)
async def eventMessage():
    if len(rocketrycfg.weeddick) == 0:
        return
    else:
        # Get Guild Scheduled Event Link from First Event in List
        guild = client.get_guild(972627157513797643)
        ScheduledEvent = guild.get_scheduled_event(int(rocketrycfg.weeddick[0]))
        unsplit_link = ScheduledEvent.url
        # Excise Event ID from Link
        split_link = unsplit_link.rpartition('/')
        linkbase = split_link[0] + split_link[1]
        for element in rocketrycfg.weeddick:
            # Create Event Link for each Element
            linky = f'{linkbase}' + f'{element}'
            # Send Event Link Message to Channel. Wait 10s between for Multiple Events
            channel = client.get_channel(991883717289197589)
            await channel.send(f'{linky}')
            time.sleep(10)
        # Clear cfg File
        rocketrycfg.weeddick = ''

client.run(DS_TOKEN)