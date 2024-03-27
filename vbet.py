from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from unidecode import unidecode
import random
import json
from datetime import datetime
from info_account import username_VBET, password_VBET
from public_func import find_matching_event

loginUrl_VBET = 'https://vbet.lat/en/'
history_url = 'https://www.vbet.lat/en/sports/pre-match/event-view/Soccer/Brazil/1792?profile=open&account=history&page=bets'

driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 20)
driver.get(loginUrl_VBET)
print('Started logging')
while True:
    try:
        driver.find_element(By.CLASS_NAME, 'sign-in').click()
        break
    except:
        pass
    sleep(1)

while True:
    try:
        driver.find_element(By.NAME, 'username').send_keys(username_VBET)
        sleep(1)
        driver.find_element(By.NAME, 'password').send_keys(password_VBET)
        sleep(1)
        driver.find_element(By.CLASS_NAME, 'entrance-form-action-item-bc').find_element(By.TAG_NAME, 'button').click()
        break
    except:
        pass
    sleep(1)

sleep(10)

driver.get('https://www.vbet.lat/en/sports/pre-match/event-view')

while True:
    try:                                 
        currency_type = driver.find_element(By.CLASS_NAME, 'wallet-content-currency').text

        if str(currency_type) != 'USD':
            driver.find_element(By.CLASS_NAME, 'wallet-button-arrow').click()
            sleep(5)
            driver.find_element(By.CLASS_NAME, 'wallet-currency-item').click()
            sleep(5)
        else:
            available = float(driver.find_element(By.CLASS_NAME, 'hdr-user-info-texts-bc').text.split(' ')[0])
            with open('_balance.json', 'r') as fp:
                balance = json.load(fp)
            balance['VBET'] = available
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
        Time_count = 0
        cycle = random.randint(5, 15) * 60 + random.randint(1, 59)
        driver.get('https://www.vbet.lat/en/')
        driver.get('https://www.vbet.lat/en/sports/pre-match/event-view')
    try:
        driver.find_element(By.CLASS_NAME, 'sign-in').click()
        while True:
            try:
                driver.find_element(By.NAME, 'username').send_keys(username_VBET)
                sleep(1)
                driver.find_element(By.NAME, 'password').send_keys(password_VBET)
                sleep(1)
                driver.find_element(By.CLASS_NAME, 'entrance-form-action-item-bc').find_element(By.TAG_NAME, 'button').click()
                sleep(1)
                break
            except:
                pass
            sleep(1)
    except:
        pass
    try:
        with open('_store.json', 'r') as fp:
            result = json.load(fp)
        
        if str(result)[0] == '{':
            bookie = result['bookie']
            if bookie == 'VBET':
                print('received new match event')
                Time_count = 0
                country = result['country']
                winner = result['winner']
                loser = result['loser']
                min_quota = result['min_quota']

                search_input = driver.find_element(By.CLASS_NAME, 'ss-input-bc')
                search_input.clear()
                search_input.send_keys(winner)
                sleep(5)
                wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'sport-search-result-bc')))
                sleep(5)
                while True:
                    try:
                        results = driver.find_elements(By.CLASS_NAME, 'sport-search-result-item-bc')
                        print('search result count : ', len(results))
                        for item in results:
                            element = item.find_elements(By.TAG_NAME, 'p')[1]
                            # player_name = translator.translate(element.text).text.split(' - ')
                            player_name = unidecode(element.text).split(' - ')
                            players = []
                            players.append(player_name[0])
                            players.append(player_name[1])
                        
                            index = find_matching_event(winner=winner, loser=loser, players=players)

                            if index != 2:
                                driver.execute_script("arguments[0].click();", item)
                                sleep(5)
                                break

                        if index != 2:
                            # Getting names and quota
                            try:
                                element = driver.find_element(By.CSS_SELECTOR, 'div[data-index="0"]')
                                quotas = element.find_elements(By.CLASS_NAME, 'market-odd-bc')

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
                                            stake_input = driver.find_element(By.CLASS_NAME, 'bs-bet-i-b-s-i-bc')
                                            stake_input.clear()
                                            stake_input.send_keys(amount)
                                            sleep(1)

                                            bet_button = driver.find_element(By.CLASS_NAME, 'bet-button-wrapper-bc').find_element(By.TAG_NAME, 'button')
                                            driver.execute_script("arguments[0].click();", bet_button)
                                            
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
                                                    driver.find_element(By.CLASS_NAME, 'u-i-p-c-filter-footer-bc').find_element(By.TAG_NAME, 'button').click()
                                                    break
                                                except:
                                                    pass
                                                sleep(1)
                                                
                                            while True:
                                                try:
                                                    frame = driver.find_element(By.CLASS_NAME, 'betHistoryList-tbody')
                                                    id = frame.find_element(By.CLASS_NAME, 'betHistory-Id')
                                                    db_info['id'] = id.text
                                                    break
                                                except:
                                                    pass
                                                sleep(1)

                                            with open('_db.json', 'w') as fp:
                                                json.dump(db_info, fp)

                                            with open('_balance.json', 'r') as fp:
                                                balance = json.load(fp)
                                            balance['VBET'] = float(driver.find_element(By.CLASS_NAME, 'hdr-user-info-texts-bc').text.split(' ')[0])
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
                            except:
                                with open('_store.json', 'w') as fp:
                                    json.dump('there are no matching players', fp)
                                print('there are no matching players')
                        else:
                            with open('_store.json', 'w') as fp:
                                json.dump('there are no matching players', fp)
                            print('there are no matching players')
                        break
                    except:
                        pass

                    try:
                        driver.find_element(By.CLASS_NAME, 'sport-search-result-bc').find_element(By.CLASS_NAME, 'empty-b-text-v-bc')
                        with open('_store.json', 'w') as fp:
                            json.dump('there are no matching players', fp)
                        print('search result count : 0')
                        print('there are no matching players')
                        break
                    except:
                        pass
                    sleep(1)

                driver.get('https://www.vbet.lat/en/sports/pre-match/event-view')

        if str(result) == 'history':
            with open('_status.json', 'r') as fp:
                status_array = json.load(fp)
            driver.get(history_url)
            while True:
                try:
                    frames = driver.find_elements(By.CLASS_NAME, 'betHistoryList-tbody')
                    for frame in frames:                        
                        id = driver.find_element(By.CLASS_NAME, 'betHistory-Id')
                        status = driver.find_element(By.CLASS_NAME, 'bethistoryListEl-item-status')
                        for index in status_array:
                            if str(index['bookie']) != 'VBET':
                                continue
                            if str(index['bet_id']) == id.text():
                                index['status'] = status.text()
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