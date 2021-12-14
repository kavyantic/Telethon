import os
import telethon.errors.rpcerrorlist as tlerr
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser ,ChannelParticipantsAdmins
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest,JoinChannelRequest
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


for name in admins:
    admins[name](JoinChannelRequest('https://t.me/TGAthGreatAwakening'))