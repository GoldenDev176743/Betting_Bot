from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC

import json
from unidecode import unidecode
import subprocess
from datetime import datetime
import sqlite3
import random
from info_account import username_WinnarOdds, password_WinnarOdds
from public_func import send_mail

from telegram import Bot
from telegram.constants import ParseMode
import asyncio

bot_token = 

icons = {
    "MARATHON" : '🥎',
    "MEGAPARI" : '🌏',
    "PINNACLE" : '🪀',
    "VBET" : '🎾'
}

message_template  = '''🎾   {bookie} 
{country}   winner : {winner} - loser : {loser}
quota: {quota}   amount: ${amount}   benefit: ${benefit}   BET ID: {id}'''

# ------------------------- Initialization ---------------------------------#
min_amount = { "MARATHON" : 0.21, "MEGAPARI" : 0.21, "PINNACLE" : 0.21, "VBET" : 0.21}

betting_sites = ['pinnacle', 'vbet', 'marathon']

with open('_store.json', 'w') as fp:
    json.dump('0', fp)

with open('_db.json', 'w') as fp:
    json.dump('0', fp)

connection = sqlite3.connect("info.db")
cursor = connection.cursor()

# --------------------- Sign-in to betting sites ---------------------------------#
for site in betting_sites:
    print('Started logging into {}.'.format(site))
    subprocess.Popen(["python", site + ".py"], stdout=subprocess.PIPE)
    while True:
        result = ''
        try:
            with open('_store.json', 'r') as fp:
                result = json.load(fp)
        except:
            pass
        if result == '1':
            with open('_store.json', 'w') as fp:
                json.dump('0', fp)
            break
        sleep(1)
#--------------------- Running the app ---------------------------------#
subprocess.Popen(["python", "history.py"], stdout=subprocess.PIPE)

sleep(5)

print('Start logging into winnerodds')
loginUrl_WinnarOdds = 'https://app.winnerodds.com/login'

driver = webdriver.Chrome()
driver.maximize_window()

driver.get(loginUrl_WinnarOdds)
wait = WebDriverWait(driver, 20)

driver.get(loginUrl_WinnarOdds)
sleep(random.randint(1, 10))

next_button = wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'button')))
driver.find_elements(By.TAG_NAME, 'input')[0].send_keys(username_WinnarOdds)
sleep(random.randint(1, 10))
driver.find_elements(By.TAG_NAME, 'input')[1].send_keys(password_WinnarOdds)
sleep(random.randint(1, 10))
next_button.click()


def main():
    sleep(random.randint(10, 20))
    try:
        match_count = len(driver.find_elements(By.CLASS_NAME, 'match'))
    except:
        match_count = 0

    for index in range(match_count):
        while True:
            try:
                with open('_store.json', 'r') as fp:
                    result = json.load(fp)
            except:
                pass
            if str(result) == '0':  
                break
            sleep(1)    
        
        print('--------------- ', datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ' -------------------------')
        match = driver.find_element(By.CLASS_NAME, 'match')
        country = match.find_element(By.CLASS_NAME, 'country').text
        winner = match.find_element(By.CLASS_NAME, 'player-info-name').text
        loser = match.find_element(By.CLASS_NAME, 'players-info-home').text
        if winner == loser:
            loser = match.find_element(By.CLASS_NAME, 'players-info-away').text
        min_quota = match.find_element(By.CLASS_NAME, 'match-cmin-quota').text

        winner = unidecode(winner)
        loser = unidecode(loser)

        odd = match.find_element(By.CLASS_NAME, 'odd')
        bookie = odd.find_element(By.CLASS_NAME, 'bookie').text
        origin_quota = odd.find_element(By.CLASS_NAME, 'match-odd-quota').text
        try:
            amount = odd.find_element(By.CLASS_NAME, 'amount').text.split('$')[0]     
        except:      
            match.find_element(By.CLASS_NAME,'icon-eye-open').click() 
            continue

        match_info = {}
        match_info['country'] = country
        match_info['bookie'] = bookie
        match_info['winner'] = winner
        match_info['loser'] = loser
        match_info['min_quota'] = min_quota
        match_info['origin_quota'] = origin_quota
        match_info['amount'] = amount
        
        with open('_balance.json', 'r') as fp:
            balance = json.load(fp)

        if float(balance[bookie]) >= float(amount):
            odd.click()

            with open('_store.json', 'w') as fp:
                json.dump(match_info, fp)

            print(match_info)

            while True: 
                sleep(1)
                try:
                    with open('_store.json', 'r') as fp:
                        result = json.load(fp)
                except:
                    pass
                if str(result)[0] == '1':
                    updated_quota = str(result).split(' ')[1]
                    print('received quota to be updated! ', origin_quota, '->', updated_quota)
                    save_quota = driver.find_element(By.NAME, 'quota')
                    save_quota.clear()
                    save_quota.send_keys(updated_quota)
                    sleep(1)
                    save_amount = driver.find_element(By.NAME, 'amount')
                    save_amount_value = save_amount.get_attribute('value')
                    if float(save_amount_value) >= min_amount[bookie]:   
                        with open('_store.json', 'w') as fp:
                            json.dump('2 ' + save_amount_value, fp)
                        print('Amount sent for a bet! ', amount, '->', save_amount_value)
                        print('waiting for the bet placing...')
                        
                        time_count = 0
                        isSent = False
                        while True:
                            res = ''
                            try:
                                with open('_store.json', 'r') as fp:
                                    res = json.load(fp)
                            except:
                                pass
                            if str(res) == '0':
                                driver.find_element(By.CLASS_NAME, 'fnt-upper').click()  
                                message = 'successfully saved with {}$!'.format(str(save_amount_value))
                                print(message)
                                send_mail(message)                         
                                break
                            sleep(1)  
                            time_count += 1
                            if not isSent and time_count >= 120:
                                isSent = True
                                message = 'The bot is running incorrectly.'
                                print(message)
                                send_mail(message)      
                    else:
                        with open('_store.json', 'w') as fp:
                            json.dump('amount is less than min', fp)
                        driver.find_element(By.CLASS_NAME, 'icon-close').click() 
                        sleep(random.randint(1, 10))
                        match.find_element(By.CLASS_NAME,'icon-eye-open').click()
                        sleep(random.randint(1, 10))
                        message = 'The match event is hidden because amount is less than min amount {}$'.format(min_amount[bookie])
                        print(message)
                        send_mail(message)      
                    break
                if str(result) == "quota is less than minimum" or str(result) == "there are no matching players":
                    driver.find_element(By.CLASS_NAME, 'icon-close').click() 
                    sleep(random.randint(5, 10))
                    match.find_element(By.CLASS_NAME,'icon-eye-open').click()
                    sleep(random.randint(5, 10))
                    with open('_store.json', 'w') as fp:
                        json.dump('0', fp)
                    message = 'The match event is hidden because {}.'.format(str(result))
                    print(message)
                    send_mail(message)    
                    break
        else:
            message = 'balance of {} site is less than the amount to be placed!'.format(bookie)
            print(message)      
            send_mail(message)     
            break 
        if 'history' not in str(result):
            with open('_db.json', 'r') as fp:
                db = json.load(fp)
            if str(db)[0] == '{':
                cursor.execute("insert into data(date_time,bookie,country,winner,loser,quota,amount,benefit,bet_id,status) values(?,?,?,?,?,?,?,?,?,?)", (db['date_time'],db['bookie'],db['country'],db['winner'],db['loser'],db['quota'],db['amount'],db['benefit'],db['id'],db['status']))
                connection.commit()
                print('Successfully saved to database.')
                with open('_db.json', 'w') as fp:
                    json.dump('0', fp)
                db['icon'] = icons[db['bookie']]
                asyncio.run(send_message_to_channel(message_template.format(**db)))
        wait_time = random.randint(1, 10) * 6
        sleep(wait_time)
    with open('_gmail.json', 'w') as fp:
        json.dump('0', fp)
    print('waiting for receiving a new match event from Gmail...')
    
if __name__ == "__main__":
    main()
    while True:      
        try:
            with open('_gmail.json', 'r') as fp:
                result = json.load(fp)
            if str(result) == '1':
                driver.refresh()
                main()
        except:
            pass    
        sleep(1)