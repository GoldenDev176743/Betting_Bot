from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

import json
from unidecode import unidecode
import os
import os.path
import resend
import sqlite3
import pyautogui

# 6-rks  harryporter319193@gmail.com
resend.api_key = 
# resend.api_key = "re_C7NcMz3r_Ldh52znYH7y7cfXHcjLQrJaP"     # 5-hyc   https://resend.com/api-keys

# loginUrl_WinnarOdds = 'https://app.winnerodds.com/login'
# username_WinnarOdds = 'davidabadi23'
# password_WinnarOdds = 'david27624818'

# driver = webdriver.Chrome()
# driver.maximize_window()

# driver.get(loginUrl_WinnarOdds)
# sleep(5)

# Inputs = driver.find_elements(By.TAG_NAME, 'input')
# Inputs[0].send_keys(username_WinnarOdds)
# sleep(1)
# Inputs[1].send_keys(password_WinnarOdds)
# sleep(1)
# driver.find_element(By.TAG_NAME, 'button').click()
# print('winnerodds login has been successfully completed.')
# sleep(5)
# driver.get('https://app.winnerodds.com/odds/football')

# sleep(30)
# driver.find_element(By.CLASS_NAME, 'icon-close').click()
# sleep(20)
# driver.find_element(By.CLASS_NAME,'icon-eye-open').click()
# sleep(10)

# message = "why don't you see slack?"

# params = {
#     "from": "MBF HarryPorter <onboarding@resend.dev>",
#     "to": ["harryporter319193@gmail.com"],
#     "subject": "Notification",
#     "html": "<strong>{}</strong>".format(message),
#     "headers": {
#     "X-Entity-Ref-ID": "123456789"
#     },
#     "attachments": [],
# }
# resend.Emails.send(params)


# frames = []
# if len(frames)== 0:
#     print('OK')
# else:
#     print('afd')
# dirPath = os.path.dirname(os.path.realpath(__file__))
# connection = sqlite3.connect("info.db")
# cursor = connection.cursor()
# db_PrevNumber = 0
# # with open(os.path.join(dirPath, '_db.json'), 'r') as fp:
# #     db = json.load(fp)
# # if db_PrevNumber != int(db['no']):
# #     db_PrevNumber = int(db['no'])
# #     cursor.execute("insert into data(date_time,bookie,country,winner,loser,quota,amount,benefit,bet_id,status) values(?,?,?,?,?,?,?,?,?,?)", (db['date_time'],db['bookie'],db['country'],db['winner'],db['loser'],db['quota'],db['amount'],db['benefit'],db['id'],db['status']))
# #     connection.commit()
# #     print('added to database.')
# with open(os.path.join(dirPath, '_db.json'), 'r') as fp:
#     db = json.load(fp)
# if str(db)[0] == '{':
#     cursor.execute("insert into data(date_time,bookie,country,winner,loser,quota,amount,benefit,bet_id,status) values(?,?,?,?,?,?,?,?,?,?)", (db['date_time'],db['bookie'],db['country'],db['winner'],db['loser'],db['quota'],db['amount'],db['benefit'],db['id'],db['status']))
#     connection.commit()
#     with open('_db.json', 'w') as fp:
#         json.dump('', fp)
#     print('Added to database.')

# print('loss' == 'Loss')
# print(unidecode('Yan Bai'))

# result = 'historysadff'
# if 'history' not in str(result):
#     print('ok')
# else:
#     print('false')

# json_list = []

# if len(json_list) == 0:
#     print('0')
# else:
#     print('ppp')

# while True:
#     x, y = pyautogui.position()
#     print(x, y)
#     sleep(1)


# count = 0
# import json
# with open('_gmail.json','w') as fp:
# 	json.dump('1',fp)

# with open('_gmail.json', 'r') as fp:
#     result = json.load(fp)
# print(result)

# from public_func import send_mail, find_matching_event

# print(send_mail('sfad'))
# print(find_matching_event('aaa adfa', 'afd iuafd', ['adge fae', 'afdffe atgad']))
# from telegram import Bot
# from telegram.constants import ParseMode
# import asyncio

# icons = {
#     "MARATHON" : '🥎',
#     "MEGAPARI" : '🌏',
#     "PINNACLE" : '🪀',
#     "VBET" : '🎾'
# }

# message_template  = '''🎾   {bookie} 
# {country}   winner : {winner} - loser : {loser}
# quota: {quota}   amount: ${amount}   benefit: ${benefit}   BET ID: {id}'''

# david_token = '6593729339:AAEuuqutituMNXEzihQvFNm3i8hQNOQ7i2Y'

# async def send_message_to_channel(message):
#     try:
#         bot = Bot(token=david_token)
#         async with bot:
#             # await bot.send_message(chat_id='1089950711', text=message, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
#             await bot.send_message(chat_id='6158733873', text=message, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

#     except Exception as e:
#         print("An error occurred while sending the message:", str(e))
# if __name__ == "__main__":
#     with open('_db.json', 'r') as fp:
#         db = json.load(fp)
#     db['id'] = '12345'
#     db['benefit'] = '12345'
#     db['quota'] = '12345'
#     asyncio.run(send_message_to_channel(message_template.format(**db)))
#     # asyncio.run(send_message_to_channel('Hello'))

print(round(float('123.3434354543542'), 2))