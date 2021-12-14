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

# Configuration
id = "1577351832"
path = './drafted'
admin_index =0




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



# Task with specific Admin account 
group_id_in_common_list = list(set.intersection(*map(set, all_members_group_list)))

id = "1577351832"
common_groups = {}

for group_id in all_members_group_list[admin_index]:
    if(group_id in group_id_in_common_list):
        common_groups[group_id]=all_members_group_list[admin_index][group_id]



target_group = common_groups[id]
group_objects_for_admins = {}
for admin_key in admins:
    group_entity = admins[admin_key].get_entity(target_group.username)
    id = group_entity.id
    access_hash = group_entity.access_hash 
    target_group_entity = InputPeerChannel(id,access_hash)
    group_objects_for_admins[admin_key] = target_group_entity



my_group_participants = admins[list(admins)[admin_index]].get_participants(group_objects_for_admins[list(admins)[admin_index]], aggressive=True)
my_group_participants_user_id = [user.id for user in my_group_participants]

path = './drafted'
files = os.listdir(path)
csv_file = ""
for file in files:
        if(file[::-1].split(".")[0][::-1]=="csv"):
            csv_file = path+'/'+file
            break

users = []
with open(csv_file, encoding='UTF-8') as f:
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






admins_length = len(admins)
min_sleep_time = 8/admins_length
# max_sleep_time = 100/admins_length
key_names = list(admins)
logf = open("download.log", "w")


for idx,user in enumerate(users):
        if user["id"] in my_group_participants_user_id or user['username'] == "" or user['username'][-3:]=="bot":
                    continue
        client_index = (idx+admins_length)%admins_length
        with admins[key_names[client_index]] as client:
            print(key_names[client_index]," ",end="")
            try: 
                print ("Adding {}".format(user['name']))
                # user_to_add = client.get_input_entity(user['username'])
                user_to_add =  InputPeerUser(user['id'], user['access_hash'])
                # user_to_add =  client.get_entity(user_to_add)

                client(InviteToChannelRequest(group_objects_for_admins[key_names[client_index]],[user_to_add]))
                print(f"Successfull Waiting {min_sleep_time} Seconds...")
                time.sleep(min_sleep_time)
            except PeerFloodError:
                print(f"{key_names[client_index]} : Getting Flood Error from telegram. Removing him now now. Please try again after some time.")
                admins.pop(key_names[client_index])
            except UserPrivacyRestrictedError:
                print(f"{key_names[client_index]} : The user's privacy settings do not allow you to do this. sleeping for {min_sleep_time} seconds")
                time.sleep(min_sleep_time)
            # except tlerr.ChannelInvalidError:
            #     print(f"{key_names[client_index]} : Skipping due to some unknown error. sleeping for {min_sleep_time} seconds ")
            #     time.sleep(min_sleep_time)
            except BufferError:
                print(f"{key_names[client_index]} : Buffer Error")
                time.sleep(20)
            except tlerr.UserChannelsTooMuchError:
                print(f"{key_names[client_index]} : UserChannelsTooMuchError")
                time.sleep(min_sleep_time)
            except ValueError:
                continue
            except tlerr.UserIdInvalidError: 
                time.sleep(2)
                print(f"{key_names[client_index]} : User Id is invalid  ") 
            except tlerr.UsernameInvalidError:
                continue
            except ConnectionError:
                input("Network conncetion falid please enter to continue : ")
                continue

            except Exception as err:
                logf.write("Failed to add with {0} \n {1}\n\n\n".format(str(key_names[client_index]), str(err)))              
                continue
