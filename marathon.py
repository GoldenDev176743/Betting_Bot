from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC

import json
import random
from datetime import datetime
from unidecode import unidecode
from info_account import username_MARATHON, password_MARATHON
from public_func import find_matching_event

loginUrl_MARATHON = 'https://www.marathonbet.com/en/?cppcids=all'
history_url = 'https://www.marathonbet.com/en/myaccount/bethistory.htm'

driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 20)
driver.get(loginUrl_MARATHON)
print('Started logging')
while True:
    try:
        driver.find_element(By.CLASS_NAME, 'auth-form__login-control').click()
        break
    except:
        pass
    sleep(1)

while True:
    try:
        login_form = driver.find_element(By.TAG_NAME, 'form')
        login_form.find_element(By.CLASS_NAME, 'phone__country').click()
        listItems = login_form.find_elements(By.CLASS_NAME, 'v-list-item')
        for item in listItems:
            if item.find_element(By.CLASS_NAME, 'country__name').text == 'Venezuela +58':
                driver.execute_script("arguments[0].click();", item)
                break
        Inputs = login_form.find_elements(By.TAG_NAME, 'input')
        Inputs[1].clear()
        Inputs[1].send_keys(username_MARATHON)
        sleep(1)
        Inputs[2].clear()
        Inputs[2].send_keys(password_MARATHON)
        sleep(1)
        driver.find_element(By.CLASS_NAME, 'login-primary-btn').click()
        break
    except:
        pass
    sleep(1)

while True:
    try:
        available = driver.find_element(By.CLASS_NAME, 'punter-balance__value')
        with open('_balance.json', 'r') as fp:
            balance = json.load(fp)
        balance['MARATHON'] = float(available.text.split(' ')[1])
        with open('_balance.json', 'w') as fp:
            json.dump(balance, fp)

        with open('_store.json', 'w') as fp:
            json.dump('1', fp)
        break
    except:
        pass
    sleep(1)
print('Login success')
sleep(10)
Time_count = 0
cycle = random.randint(5, 15) * 60 + random.randint(1, 59)
while True:
    Time_count += 1
    if Time_count >= cycle:
        cycle = random.randint(5, 15) * 60 + random.randint(1, 59)
        Time_count = 0
        driver.get('https://www.marathonbet.com/en/betting/Tennis+-+2398')
        driver.get('https://www.marathonbet.com/en/?cppcids=all')

    try:   
        driver.find_element(By.CLASS_NAME, 'auth-form__login-control')
        print(driver.current_url)
        while True:
            print('clicking...')
            try:
                driver.find_element(By.CLASS_NAME, 'auth-form__login-control').click()
                break
            except:
                pass
            sleep(1)
        while True:
            print('finding form...')
            sleep(1)
            try:
                login_form = driver.find_element(By.TAG_NAME, 'form')
                login_form.find_element(By.CLASS_NAME, 'phone__country').click()
                listItems = login_form.find_elements(By.CLASS_NAME, 'v-list-item')
                for item in listItems:
                    if item.find_element(By.CLASS_NAME, 'country__name').text == 'Venezuela +58':
                        driver.execute_script("arguments[0].click();", item)
                        break
                Inputs = login_form.find_elements(By.TAG_NAME, 'input')
                Inputs[1].clear()
                Inputs[1].send_keys(username_MARATHON)
                sleep(1)
                Inputs[2].clear()
                Inputs[2].send_keys(password_MARATHON)
                sleep(1)
                driver.find_element(By.CLASS_NAME, 'login-primary-btn').click()
                sleep(5)
                break
            except:
                pass
    except:
        pass
    try:
        with open('_store.json', 'r') as fp:
            result = json.load(fp)

        if str(result)[0] == '{':
            bookie = result['bookie']
            if bookie == 'MARATHON':
                print('received new match event')
                Time_count = 0
                country = result['country']
                winner = result['winner']
                loser = result['loser']
                min_quota = result['min_quota']

                splitted_name = winner.split(' ')
                search_key = ''
                for split in splitted_name:
                    if len(split) >= 3:
                        search_key = split
                        break
                searchUrl = 'https://www.marathonbet.com/en/search.htm?searchText=' + search_key
                driver.get(searchUrl)
                sleep(5)

                wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'search-page')))

                try:
                    driver.find_elements(By.CLASS_NAME, 'tab-labels')[2].click()
                except:
                    pass

                sleep(5)

                while True:
                    try:
                        results = driver.find_elements(By.CLASS_NAME, 'coupon-row')
                        print('search result count : ', len(results))
                        for item in results:
                            isMatched = False
                            if 'Tennis' in item.get_attribute('data-event-path'):
                                # Getting names and quota
                                player = item.find_elements(By.CLASS_NAME, 'member-link')
                                quotas = item.find_elements(By.CLASS_NAME, 'height-column-with-price')

                                players = []
                                for name in player:
                                    player_name = unidecode(name.text)
                                    players.append(player_name)

                                index = find_matching_event(winner=winner, loser=loser, players=players)

                                if index != 2:
                                    isMatched = True
                                    if float(min_quota) <= float(quotas[index].text):
                                        selected_quota = quotas[index]
                                        selected_quota_value = quotas[index].text

                                        with open('_store.json', 'w') as fp:
                                            json.dump('1 ' + selected_quota_value, fp)

                                        while True:
                                            try:
                                                with open('_store.json', 'r') as fp:
                                                    result = json.load(fp)
                                            except:
                                                pass
                                            if str(result)[0] == '2':
                                                amount = str(result).split(' ')[1]
                                                driver.execute_script("arguments[0].click();", selected_quota)
                                                sleep(5)
                                                stake_input = driver.find_element(By.CLASS_NAME, 'stake-input')
                                                stake_input.clear()
                                                stake_input.send_keys(amount)
                                                sleep(1)
                                                driver.find_element(By.CLASS_NAME, 'btn-place-bet').click()

                                                while True:
                                                    try:
                                                        bet_button = driver.find_element(By.ID, 'ok-button')
                                                        driver.execute_script("arguments[0].click();", bet_button)
                                                        break
                                                    except:
                                                        pass
                                                    sleep(1)

                                                curr_time = datetime.now()

                                                with open('_db.json', 'r') as fp:
                                                    db = json.load(fp)

                                                db_info = {}
                                                db_info['date_time'] = curr_time.strftime("%Y-%m-%d %H:%M:%S")
                                                db_info['bookie'] = bookie
                                                db_info['country'] = country
                                                db_info['winner'] = winner
                                                db_info['loser'] = loser
                                                db_info['quota'] = selected_quota_value
                                                db_info['amount'] = amount
                                                db_info['benefit'] = round(((float(selected_quota_value) - 1) * float(amount)), 2)
                                                db_info['status'] = 'Unsettled'
                                                sleep(5)
                                                driver.get(history_url)
                                                while True:
                                                    try:
                                                        frame = driver.find_element(By.CLASS_NAME, 'history-result-main')
                                                        id = frame.find_element(By.CLASS_NAME, 'bet-number')
                                                        db_info['id'] = id.text                                                        
                                                        break
                                                    except:
                                                        pass
                                                    sleep(1)

                                                with open('_db.json', 'w') as fp:
                                                    json.dump(db_info, fp)

                                                with open('_balance.json', 'r') as fp:
                                                    balance = json.load(fp)
                                                available = driver.find_element(By.CLASS_NAME, 'punter-balance__value')
                                                balance['MARATHON'] = float(available.text.split(' ')[1])
                                                with open('_balance.json', 'w') as fp:
                                                    json.dump(balance, fp)

                                                with open('_store.json', 'w') as fp:
                                                    json.dump('0', fp)
                                                break
                                            if str(result) == 'amount is less than min':
                                                with open('_store.json', 'w') as fp:
                                                    json.dump('0', fp)
                                                break
                                            sleep(1)
                                    else:
                                        with open('_store.json', 'w') as fp:
                                            json.dump('quota is less than minimum', fp)
                                        print('quota is less than minimum')
                                    break
                        if not isMatched:
                            with open('_store.json', 'w') as fp:
                                json.dump('there are no matching players', fp)                            
                            print('there are no matching players')
                        break
                    except:
                        pass

                    try:
                        driver.find_element(By.CLASS_NAME, 'v-not-found')
                        with open('_store.json', 'w') as fp:
                            json.dump('there are no matching players', fp)
                        print('search result count : 0')
                        print('there are no matching players')
                        break
                    except:
                        pass
                    sleep(1)

                driver.get('https://www.marathonbet.com/en/?cppcids=all')

        if str(result) == 'history':
            with open('_status.json', 'r') as fp:
                status_array = json.load(fp)
            driver.get(history_url)
            while True:
                try:
                    frames = driver.find_elements(By.CLASS_NAME, 'history-result-main')
                    for frame in frames:
                        id = frame.find_element(By.CLASS_NAME, 'bet-number')
                        status = frame.find_element(By.CLASS_NAME, 'open-bet')
                        for index in status_array:
                            if str(index['bookie']) != 'MARATHON':
                                continue
                            if str(index['bet_id']) == id.text():
                                try:
                                    status = frame.find_element(By.CLASS_NAME, 'bet-icon-status')
                                    src = status.find_element(By.TAG_NAME, 'img').get_attribute('src')
                                    if 'win' in src:
                                        db_info['status'] = 'Won'
                                    if 'lose' in src:
                                        db_info['status'] = 'Loss'
                                except:
                                    db_info['status'] = 'Unsettled'
                                break
                    break
                except:
                    pass
                sleep(1)
            with open('_store.json', 'r') as fp:
                store = json.load(fp)
            with open('_store.json', 'w') as fp:
                json.dump(str(store) + 'done', fp)
    except:
        pass
    sleep(1)