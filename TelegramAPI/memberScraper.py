from telethon import TelegramClient ,events
from telethon.tl.types import InputPeerEmpty
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.functions.channels import GetParticipantsRequest
import asyncio
from constants import api_id, api_hash, session_name , bot_token, phone_number
import csv

client = TelegramClient("sessions/"+session_name, api_id, api_hash)
# client.start(bot_token=bot_token)
client.connect()


def authorize():
    if client.is_user_authorized():
        client.send_code_request(phone_number)
        client.sign_in(phone_number, input('Enter the code: '))
        print("Authorized as scraper")
    else :
        print("Could not Authorize")




async def getChats():
    result = await client(GetDialogsRequest(
             offset_date=None,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=200,
             hash = 0
         ))
    return result.chats

async def getUsers(channel_username=1570400354):
    try:
        result = await client(GetParticipantsRequest(
                channel=channel_username, 
                filter=ChannelParticipantsSearch(''), 
                offset=0, 
                limit=200,
                hash=0
                ))
    except TypeError:
        print("please enter a valid channel ID or Name")
        return None
    return result.users


def storeUsersInCsv(channel_id,csv_file=None):
    if(not csv_file):
        pass

async def main():  
    chats = await getChats()
    for i in chats:
           print(str(type(i))+" : "+i.title)
            

with client:
    client.loop.run_until_complete(main())