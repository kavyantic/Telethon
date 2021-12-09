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
phone = all_admins[0]["phone"]    # YOUR PHONE NUMBER, INCLUDING COUNTRY CODE
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


for user in users:
    if user['username'] == "":
                        continue
    try:
        user_to_add = main_client.get_input_entity(user['username']) 
    except ValueError:
        print("No user with this Username")
        continue
    # user_to_add =  InputPeerUser(user['id'], user['access_hash'])
    try:
         user = main_client.get_entity(user_to_add)
    except KeyError:
        print("skipped")
        continue
    print(user.stringify())
