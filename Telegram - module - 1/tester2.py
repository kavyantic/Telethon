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


admins = {}
for admin in all_admins:
        api_id = admin["api_id"]
        api_hash = admin["api_hash"]
        phone = admin["phone"]
        new_admin = TelegramClient("./sessions/"+phone, api_id, api_hash)         
        new_admin.connect()
        if not new_admin.is_user_authorized():
            new_admin.send_code_request(phone)
            new_admin.sign_in(phone, input(f'Enter the code for {phone} : '))
        admins[f'{new_admin.get_me().first_name}'] = new_admin

print(admins)



all_members_group_list = []
group_key_list = []
for admin in admins:
    chats = []
    last_date = None
    chunk_size = 10
    groups=[]

    result = admins[admin](GetDialogsRequest(
            offset_date=last_date,
            offset_id=0,
            offset_peer=InputPeerEmpty(),
            limit=chunk_size,
            hash = 0
        ))
    groups_with_id = {str(group.id):group for group in result.chats}
    group_keys = [group.id for group in result.chats]
    group_key_list.append(group_keys)
    all_members_group_list.append(groups_with_id)

# for group in all_members_group_list:
#     print(group)
group_id_in_common_list = list(set.intersection(*map(set, all_members_group_list)))

id = "1660268519"

for group in all_members_group_list[0]:
    if(group in group_id_in_common_list):
        print(all_members_group_list[0][group].title ," : ",all_members_group_list[0][group].id)