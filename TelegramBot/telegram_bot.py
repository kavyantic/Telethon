import telebot
# PyTelegramBotApi
from birthday_reminder import reminder
from constants import bot_token
import threading
import requests
import csv
import os


bot = telebot.TeleBot(bot_token)
BDreminder = reminder(bot)
files = []
current_user_data = []



@bot.message_handler(commands=['start', 'help'])
def start(msg):
    bot.reply_to(msg,'''List of available commands :
        /me    -    sends user details
        /save_csv  - send as caption with a csv file to save
        /show_files - shows the available user files
    ''')

# @bot.message_handler(commands=["load_users"])



@bot.message_handler(func=lambda msg:msg.caption == "/save_csv")
def save_document(message):
    if(message.content_type=="document"):
        file_info = bot.get_file(message.document.file_id)
        file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(bot_token, file_info.file_path))
        open(f'users-csv/{message.document.file_name}', 'wb').write(file.content)
        bot.reply_to(message, "This file has been saved")




@bot.message_handler(commands=["show_user_files"])
def show_users(message): 
    files = os.listdir("./users-csv")
    message_string = ''' '''
    for idx,file in enumerate(files):
        string = f'{idx} : {file}\n'
        message_string+=string
    bot.reply_to(message,message_string)


@bot.message_handler(commands=['load_file'])
def load_document(message):
    try:
        files = os.listdir("./users-csv")
        file_index = message.text.split(" ")[1]
        file = files[int(file_index)]
        csv_file = open(f"./users-csv/{file}", encoding='UTF-8') 
        rows = csv.reader(csv_file,delimiter=",",lineterminator="\n")
        next(rows, None)
        for row in rows:
                user = {}
                user['id'] =  (row[1])
                user['birth day'] = (row[2])
                current_user_data.append(user)
        bot.reply_to(message,file+" loaded")
        
    except TypeError:
        bot.reply_to(message,"please enter a available number")


@bot.message_handler(commands=['show_five'])
def show(message):
    print(current_user_data)
    bot.reply_to(message,str(current_user_data[:20]))
        

@bot.message_handler(func=lambda msg:msg.caption=="/send_to_all",content_types=['text','audio','photo','document','video',])
def broadcast_to_all(message):
        if(message.content_type=="text"):
             bot.reply_to(message,current_user_data)


  



thread1 = threading.Thread(target=bot.polling)
# thread2 = threading.Thread(target=BDreminder.remind)

thread1.start()
# thread2.start()

