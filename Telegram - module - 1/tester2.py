import os
import telethon.errors.rpcerrorlist as tlerr
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser ,ChannelParticipantsAdmins
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import sys
import csv
import traceback
import time
import random
import re
from accounts import all_admins
import sqlite3



api_id = all_admins[0]["api_id"]
api_hash = all_admins[0]["api_hash"]
phone = all_admins[0]["phone"]    
main_client = TelegramClient("sessions/"+phone, api_id, api_hash)
main_client.connect()


main_client.connect()
if not main_client.is_user_authorized():
    main_client.send_code_request(phone)
    main_client.sign_in(phone, input('Enter the code: '))


users = []
input_file = './members--tga-signup-now-livandu-com-go-to-livanduchat.csv'
with open(input_file, encoding='UTF-8') as f:
        rows = csv.reader(f,delimiter=",",lineterminator="\n")
        next(rows, None)
        for row in rows:
            user = {}
            user['username'] = row[0]
            user['name'] = row[3]
            try:
                user['id'] = int(row[1])
                user['access_hash'] = int(row[2])
            except IndexError:
                print ('users without id or access_hash')
            users.append(user)

chats = []
last_date = None
chunk_size = 200
groups=[]

for dialog in main_client.iter_dialogs():
    # if not dialog.is_group and dialog.is_channel:
        print(dialog.stringify())
# 
# target_group_entity = InputPeerChannel(target_group.id,target_group.access_hash)


# result = main_client(GetDialogsRequest(
#             offset_date=last_date,
#             offset_id=0,
#             offset_peer=InputPeerEmpty(),
#             limit=chunk_size,
#             hash = 0
#         ))

# print(result.stringify())