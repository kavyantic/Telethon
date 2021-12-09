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
if not main_client.is_user_authorized():
    main_client.send_code_request(phone)
    main_client.sign_in(phone, input('Enter the code: '))

def loadAdmins(group):
    admins_list = []
    real_channel_admins = main_client.iter_participants(group, filter=ChannelParticipantsAdmins)
    admins_list.append(main_client)
   
    for admin in all_admins:
        try:
            api_id = admin["api_id"]
            api_hash = admin["api_hash"]
            phone = admin["phone"]
            new_admin = TelegramClient("./sessions/"+phone, api_id, api_hash)         
            new_admin.connect()
            if not new_admin.is_user_authorized():
                new_admin.send_code_request(phone)
                new_admin.sign_in(phone, input('Enter the code: '))
            for real_admin in real_channel_admins:
                if(new_admin.get_me().id):
                    admins_list.append(new_admin)  
        except sqlite3.OperationalError:
            print(f"Clinet ({phone}) has already been logged.")
            continue
    return admins_list


def add_users_to_group():
    
    files = os.listdir()
    csvFiles = []
    for file in files:
        if(file[::-1].split(".")[0][::-1]=="csv"):
            csvFiles.append(file)

    print("Choose a file to load members:")
    for idx,csv_file in enumerate(csvFiles):
        print(f"{idx} - {csv_file}")

    
    input_file = "./" + csvFiles[int(0)]
    users = []
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

    #random.shuffle(users)
    chats = []
    last_date = None
    chunk_size = 10
    groups=[]

    result = main_client(GetDialogsRequest(
                offset_date=last_date,
                offset_id=0,
                offset_peer=InputPeerEmpty(),
                limit=chunk_size,
                hash = 0
            ))
    chats.extend(result.chats)
    print([i.stringify() for i in result.dialogs])

    for chat in chats:
        try:
                 groups.append(chat)
        except:
            continue
    if(len(groups)==0):
        print("\nYou are not admin in any group yet breaking.\n")
        return
    print('\nChoose a group to add members:\n')
    
    for idx,group in enumerate(groups):
        print(str(idx) + '- ' + group.title)

    g_index = input("Enter a Number: ")
    target_group=groups[int(g_index)]
    print('\n\nSelected group :\t' + groups[int(g_index)].title)

    target_group_entity = InputPeerChannel(target_group.id,target_group.access_hash)
    my_group_participants = main_client.get_participants(target_group_entity, aggressive=True)
    my_group_participants_user_id = [user.id for user in my_group_participants]


    mode = 2
    error_count = 0
    admins = loadAdmins(target_group_entity)
    print(admins)
    
    
    admins_length = len(admins)
    sleep_time = 60/admins_length
    for idx,user in enumerate(users):
        client_index = (idx+admins_length)%admins_length
        with admins[client_index] as client:
            # print(client.get_me().first_name," ",end="")
            try: 
                print ("Adding {}".format(user['name']))
                if user["id"] in my_group_participants_user_id:
                    continue
                if mode == 1:
                    if user['username'] == "":
                        continue
                    user_to_add = client.get_input_entity(user['username'])
                elif mode == 2:
                    user_to_add =  InputPeerUser(user['id'], user['access_hash'])
                client(InviteToChannelRequest(target_group_entity,[user_to_add]))
                print(f"Waiting {sleep_time} Seconds...")
                time.sleep(sleep_time)
            except PeerFloodError:
                print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
                break
            except UserPrivacyRestrictedError:
                print(f"The user's privacy settings do not allow you to do this. sleeping for {sleep_time} seconds")
                time.sleep(sleep_time)
            except tlerr.ChannelInvalidError:
                print(f"Skipping due to some unknown error. sleeping for {sleep_time} seconds ")
                time.sleep(sleep_time)
            except BufferError:
                print("Buffer Error")
                time.sleep(5)
            except tlerr.UserChannelsTooMuchError:
                time.sleep(5)
            # except :
            #     traceback.print_exc()
            #     print("Unexpected Error")
            #     error_count += 1
            #     if error_count > 10:
            #         sys.exit('too many errors')
            #     continue

def scrape_users_from_group():
    chats = []
    last_date = None
    chunk_size = 200
    groups=[]
    
    result = main_client(GetDialogsRequest(
                offset_date=last_date,
                offset_id=0,
                offset_peer=InputPeerEmpty(),
                limit=chunk_size,
                hash = 0
            ))
    chats.extend(result.chats)
    
    for chat in chats:
        try:            
            # if chat.megagroup== True:
                print(chat.stringify())
                groups.append(chat)
        except:
            continue
    
    print('Choose a group to scrape members from:')
    i=0
    for g in groups:
        print(str(i) + '- ' + g.title)
        i+=1
    
    g_index = input("Enter a Number: ")
    target_group=groups[int(g_index)]
    
    print('Fetching Members...')
    all_participants = []
    all_participants = main_client.get_participants(target_group, aggressive=True)
    
    print('Saving In file...')
    with open("members-" + re.sub("-+","-",re.sub("[^a-zA-Z]","-",str.lower(target_group.title))) + ".csv","w",encoding='UTF-8') as f:
        writer = csv.writer(f,delimiter=",",lineterminator="\n")
        writer.writerow(['username','user id', 'access hash','name','group', 'group id'])
        for user in all_participants:
            if user.username:
                username= user.username
            else:
                username= ""
            if user.first_name:
                first_name= user.first_name
            else:
                first_name= ""
            if user.last_name:
                last_name= user.last_name
            else:
                last_name= ""
            name= (first_name + ' ' + last_name).strip()
            writer.writerow([username,user.id,user.access_hash,name,target_group.title, target_group.id])      
    print('Members scraped successfully.')

def show_users():
    input_file = './members-test-for-telethon.csv'
    users = []
    with open(input_file, encoding='UTF-8') as f:
        rows = csv.reader(f,delimiter=",",lineterminator="\n")
        next(rows, None)
        for row in rows:
            user = {}
            user['username'] = row[0]
            user['id'] =  (row[1])
            user['access_hash'] = (row[2])
            users.append(user)
            print(row)
            print(user)
    sys.exit('FINITO')

# print('Fetching Members...')
# all_participants = []
# all_participants = client.get_participants(target_group, aggressive=True)
print('What do you want to do:')
# mode = int(input("Enter \n1-List users in a group\n2-Add users from CSV to Group (CSV must be passed as a parameter to the script\n3-Show CSV\n\nYour option:  "))
mode = 2
if mode == 1:
    scrape_users_from_group()
elif mode == 2:
    add_users_to_group()
elif mode == 3:
    show_users()
1