from telethon import TelegramClient ,events
from telethon.tl.types import InputPeerEmpty
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.functions.channels import GetParticipantsRequest
import asyncio
from constants import api_id, api_hash, session_name , bot_token, phone_number
import csv



client = TelegramClient("sessions/"+session_name, api_id, api_hash)
client.start()


# async def main():
#     async for dialog in  client.iter_dialogs():
#         print(dialog,"has ID - ",dialog.id)

# client.loop.run_until_complete(main())


# if client.is_user_authorized():
#     print("Authorized")
#     # client.send_code_request(phone_number)
#     # client.sign_in(phone_number, input('Enter the code: '))
# else :
#     print("Could not authorize")




# async def getChats():
#     result = await client(GetDialogsRequest(
#              offset_date=None,
#              offset_id=0,
#              offset_peer=InputPeerEmpty(),
#              limit=200,
#              hash = 0
#          ))
#     return result.chats

# async def getUsersOfChannel(channel_username=1570400354):
#     result = await client(GetParticipantsRequest(
#             channel=channel_username, 
#             filter=ChannelParticipantsSearch(''), 
#             offset=0, 
#             limit=200,
#             hash=0
#             ))
#     return result.users


# def storeUserInCsv(channel_id,csv_file=None):
#     if(not csv_file):
#         pass



from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import sys
import csv
import traceback
import time
 
api_id = 123456
api_hash = 'YOUR_API_HASH'
phone = '+111111111111'
client = TelegramClient(phone, api_id, api_hash)
 
client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))
 
input_file = sys.argv[1]
users = []
with open(input_file, encoding='UTF-8') as f:
    rows = csv.reader(f,delimiter=",",lineterminator="\n")
    next(rows, None)
    for row in rows:
        user = {}
        user['username'] = row[0]
        user['id'] = int(row[1])
        user['access_hash'] = int(row[2])
        user['name'] = row[3]
        users.append(user)
 
chats = []
last_date = None
chunk_size = 200
groups=[]
 
result = client(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
         ))
chats.extend(result.chats)
 
for chat in chats:
    try:
        if chat.megagroup== True:
            groups.append(chat)
    except:
        continue
 
print('Choose a group to add members:')
i=0
for group in groups:
    print(str(i) + '- ' + group.title)
    i+=1
 
g_index = input("Enter a Number: ")
target_group=groups[int(g_index)]
 
target_group_entity = InputPeerChannel(target_group.id,target_group.access_hash)
 
mode = int(input("Enter 1 to add by username or 2 to add by ID: "))
 
for user in users:
    try:
        print ("Adding {}".format(user['id']))
        if mode == 1:
            if user['username'] == "":
                continue
            user_to_add = client.get_input_entity(user['username'])
        elif mode == 2:
            user_to_add = InputPeerUser(user['id'], user['access_hash'])
        else:
            sys.exit("Invalid Mode Selected. Please Try Again.")
        client(InviteToChannelRequest(target_group_entity,[user_to_add]))
        print("Waiting 60 Seconds...")
        time.sleep(60)
    except PeerFloodError:
        print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
    except UserPrivacyRestrictedError:
        print("The user's privacy settings do not allow you to do this. Skipping.")
    except:
        traceback.print_exc()
        print("Unexpected Error")
        continue