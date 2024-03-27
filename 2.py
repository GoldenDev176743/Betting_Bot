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
import os
import os.path
from datetime import datetime
from info_account import username_MEGAPARI, password_MEGAPARI
from public_func import send_mail, find_matching_event

loginUrl_MEGAPARI = 'https://megapari.com/en/'
history_url = 'https://megapari.com/en/office/history'

message = 'VPN is installing... Please prepare for the VPN setting.'
send_mail(message)

options = webdriver.ChromeOptions()

options.add_argument('load-extension=' + os.path.join(os.getcwd(), 'Urban VPN'))
driver = webdriver.Chrome(options=options)

driver.maximize_window()
wait = WebDriverWait(driver, 20)
# while True:
#     try:
#         with open('_store.json', 'r') as fp:
#             result = json.load(fp)
#     except:
#         pass
#     if str(result) == 'done':
#         break
#     sleep(1)

while True:
    answer = input('Finished setting up the VPN?\n')
    if answer == 'yes':
        break
    sleep(1)

driver.get(loginUrl_MEGAPARI)
print('Started logging')
window_handles = driver.window_handles
driver.switch_to.window(window_handles[1])
driver.close()
driver.switch_to.window(window_handles[0])
sleep(1)
while True:
    try:
        driver.find_element(By.CLASS_NAME, 'auth-dropdown-trigger').click()
        break
    except:
        pass
    sleep(1)

while True:
    try:
        login_form = driver.find_element(By.TAG_NAME, 'form')
        Inputs = login_form.find_elements(By.TAG_NAME, 'input')
        Inputs[0].clear()
        Inputs[0].send_keys(username_MEGAPARI)
        sleep(1)
        Inputs[1].clear()
        Inputs[1].send_keys(password_MEGAPARI)
        sleep(1)
        login_form.find_element(By.CLASS_NAME, 'auth-form-fields__submit').click()
        break
    except:
        pass
    sleep(1)

sleep(10)

try:
    verify = driver.find_element(By.CLASS_NAME, 'input__field')
    verify.send_keys('leicester')
    sleep(1)
    driver.find_element(By.CLASS_NAME, 'ui-button').click()
    sleep(5)
except:
    pass

# while True:
#     try:
#         driver.find_element(By.CLASS_NAME, 'account-select-toggle').click()
#         sleep(5)
#         driver.find_elements(By.CLASS_NAME, 'balance-dropdown__option')[1].click()
#         sleep(5)
#         driver.find_element(By.CLASS_NAME, 'popup-controls__item').click()
#         break
#     except:
#         pass
#     sleep(1)

while True:
    try:
        available = float(driver.find_element(By.CLASS_NAME, 'account-select-toggle__value').text)
        with open('_balance.json', 'r') as fp:
            balance = json.load(fp)
        balance['MEGAPARI'] = available
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
        driver.get('https://megapari.com/en/live/tennis')
        driver.get('https://megapari.com/en/')
    try:
        driver.find_element(By.CLASS_NAME, 'auth-dropdown-trigger').click()
        while True:
            try:
                login_form = driver.find_element(By.TAG_NAME, 'form')
                Inputs = login_form.find_elements(By.TAG_NAME, 'input')
                Inputs[0].clear()
                Inputs[0].send_keys(username_MEGAPARI)
                sleep(1)
                Inputs[1].clear()
                Inputs[1].send_keys(password_MEGAPARI)
                sleep(1)
                login_form.find_element(By.CLASS_NAME, 'auth-form-fields__submit').click()
                sleep(5)
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
            if bookie == 'MEGAPARI':
                print('received new match event')
                Time_count = 0
                country = result['country']
                winner = result['winner']
                loser = result['loser']
                min_quota = result['min_quota']

                search_input = driver.find_element(By.CLASS_NAME, 'search__input')
                search_input.clear()
                search_input.send_keys(winner)
                sleep(1)

                driver.find_element(By.CLASS_NAME, 'search-button').click()
                sleep(5)

                wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'games-search-modal__results')))

                sleep(5)

                while True:
                    try:
                        results = driver.find_elements(By.CLASS_NAME, 'games-search-modal-results-list__item')
                        print('search result count : ', len(results))
                        for item in results:
                            isMatched = False
                            if 'Tennis' in item.find_element(By.CLASS_NAME, 'games-search-modal-card-info__additional').text:
                                # Getting names and quota
                                player = item.find_element(By.CLASS_NAME, 'games-search-modal-card-info__main')
                                quotas = item.find_element(By.CLASS_NAME, 'games-search-modal-game-card-markets').find_elements(By.CLASS_NAME, 'market__value')

                                # player_name = translator.translate(player.text).text
                                player_name = unidecode(player.text)
                                players = player_name.split(' - ')

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
                                                sleep(1)
                                                driver.find_element(By.CLASS_NAME, 'modal__control').click()
                                                sleep(1)
                                                stake_input = driver.find_element(By.CLASS_NAME, 'ui-number-input__field')
                                                stake_input.clear()
                                                stake_input.send_keys(amount)
                                                sleep(1)

                                                bet_button = driver.find_element(By.CLASS_NAME, 'coupon-buttons').find_element(By.TAG_NAME, 'button')
                                                driver.execute_script("arguments[0].click();", bet_button)
                                                while True:
                                                    try:
                                                        confirm_button = driver.find_element(By.CLASS_NAME, 'coupon-success-modal-controls__item')
                                                        confirm_button.click()
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
                                                        frame = driver.find_element(By.CLASS_NAME, 'bets-history-coupon-row--size-m')
                                                        id = frame.find_element(By.CLASS_NAME, 'bets-history-table-row-value__value')
                                                        db_info['id'] = id.text
                                                        break
                                                    except:
                                                        pass
                                                    sleep(1)

                                                with open('_db.json', 'w') as fp:
                                                    json.dump(db_info, fp)

                                                with open('_balance.json', 'r') as fp:
                                                    balance = json.load(fp)
                                                balance['MEGAPARI'] = float(driver.find_element(By.CLASS_NAME, 'account-select-toggle__value').text)
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
                                        print('quota is less than minimum', min_quota, quotas[index].text, index)
                                    break
                        if not isMatched:
                            with open('_store.json', 'w') as fp:
                                json.dump('there are no matching players', fp)
                            print('there are no matching players')
                        break
                    except:
                        pass

                    try:
                        driver.find_element(By.CLASS_NAME, 'message-block__head')
                        with open('_store.json', 'w') as fp:
                            json.dump('there are no matching players', fp)
                        print('search result count : 0')
                        print('there are no matching players')
                        break
                    except:
                        pass
                    sleep(1)

                driver.get('https://megapari.com/en/')

        if str(result) == 'history':
            with open('_status.json', 'r') as fp:
                status_array = json.load(fp)
            driver.get(history_url)
            while True:
                try:
                    frames = driver.find_elements(By.CLASS_NAME, 'bets-history-coupon-row--size-m')
                    for frame in frames:
                        id = frame.find_element(By.CLASS_NAME, 'bets-history-table-row-value__value')
                        status = frame.find_element(By.CLASS_NAME, 'bets-history-status__text')
                        for index in status_array:
                            if str(index['bookie']) != 'MEGAPARI':
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