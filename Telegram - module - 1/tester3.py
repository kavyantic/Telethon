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

user_to_add =  InputPeerUser("1437369448", "4794309457359831081")
print(user_to_add.stringify())