from time import sleep
import csv

class reminder():
    def __init__(self,bot):
        self.bot = bot

    
   






def start_reminder_for(input_file):
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
