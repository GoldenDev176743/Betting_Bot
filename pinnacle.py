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
from info_account import username_PINNACLE, password_PINNACLE
from public_func import send_mail, find_matching_event

loginUrl_PINNACLE = 'https://www.pinnacle.com/en/'
history_url = 'https://www.pinnacle.com/en/account/bets/history'

driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 20)
driver.get(loginUrl_PINNACLE)
print('Started logging')
while True:
    try:
        login_form = driver.find_element(By.CLASS_NAME, 'style_desktop_accountContent__3M0EK')
        message = 'Logging into Pinnacle now. Please Confirm the CAPTCHA.'
        send_mail(message)

        Inputs = login_form.find_elements(By.TAG_NAME, 'input')
        Inputs[0].send_keys(username_PINNACLE)
        sleep(1)
        Inputs[1].send_keys(password_PINNACLE)
        sleep(1)
        login_form.find_element(By.TAG_NAME, 'button').click()
        break
    except:
        pass
    sleep(1)

while True:
    try:
        element = driver.find_element(By.CLASS_NAME, 'style_bankroll__1j9mF').find_element(By.TAG_NAME, 'span')
        available = float(element.text.split(' ')[0].replace(',', '.'))
        with open('_balance.json', 'r') as fp:
            balance = json.load(fp)
        balance['PINNACLE'] = available
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
        driver.get('https://www.pinnacle.com/en/account/bets/history')
        driver.get('https://www.pinnacle.com/en/')
        
    try:
        login_form = driver.find_element(By.CLASS_NAME, 'style_desktop_accountContent__3M0EK')
        Inputs = login_form.find_elements(By.TAG_NAME, 'input')
        print('Logged out')
        Inputs[0].clear()
        Inputs[0].send_keys(username_PINNACLE)
        sleep(1)
        Inputs[1].clear()
        Inputs[1].send_keys(password_PINNACLE)
        sleep(1)
        login_form.find_element(By.TAG_NAME, 'button').click()
        time_count = 0
        isSent = False
        while True:
            try:
                element = driver.find_element(By.CLASS_NAME, 'style_bankroll__1j9mF').find_element(By.TAG_NAME, 'span')
                message = 'Logged in again.'
                send_mail(message)
                break
            except:
                time_count += 1
            if not isSent and time_count >= 120:
                isSent = True
                message = 'Pinnacle is logged out. Please check out!'
                send_mail(message)
            sleep(1)
    except:
        pass

    try:
        with open('_store.json', 'r') as fp:
            result = json.load(fp)

        if str(result)[0] == '{':
            bookie = result['bookie']
            if bookie == 'PINNACLE':
                print('received new match event')
                Time_count = 0
                country = result['country']
                winner = result['winner']
                loser = result['loser']
                min_quota = result['min_quota']

                searchUrl = 'https://www.pinnacle.com/es/search/tennis/{}/participant/'.format(winner)
                driver.get(searchUrl)
                sleep(5)
                wait.until(EC.visibility_of_any_elements_located((By.TAG_NAME, 'main')))
                try:
                    favourite = driver.find_element(By.CLASS_NAME, 'style_supportFavoritesList__13pHT')
                    favourite.click()
                except:
                    pass    
                sleep(5)            

                while True:
                    try:
                        results = driver.find_elements(By.CLASS_NAME, 'style_row__OAolX')
                        print('search result count : ', len(results))
                        for item in results:
                            isMatched = False
                            # Getting names and quota
                            player = item.find_elements(By.CLASS_NAME, 'style_participantName__2S6gW')
                            quota = item.find_elements(By.TAG_NAME, 'span')
                            players = []
                            for name in player:
                                # player_name = translator.translate(name.text).text
                                player_name = unidecode(name.text)
                                if ' (' in player_name:
                                    players.append(player_name.split(" (")[0])
                                else:
                                    players.append(player_name)
                            quotas = []
                            quotas.append(quota[4])
                            quotas.append(quota[5])

                            if '+' not in quotas[0].text:
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
                                            container = driver.find_element(By.ID, 'scroll-container')
                                            stake_input = container.find_element(By.TAG_NAME, 'input')
                                            stake_input.clear()
                                            stake_input.send_keys(amount)
                                            sleep(1)

                                            bet_button = container.find_elements(By.TAG_NAME, 'button')[1]
                                            driver.execute_script("arguments[0].click();", bet_button)
                                            sleep(1)

                                            with open('_balance.json', 'r') as fp:
                                                balance = json.load(fp)
                                            available = driver.find_element(By.CLASS_NAME, 'style_bankroll__1j9mF').find_element(By.TAG_NAME, 'span')
                                            balance['PINNACLE'] = float(available.text.split(' ')[0].replace(',', '.'))
                                            with open('_balance.json', 'w') as fp:
                                                json.dump(balance, fp)

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
                                                    frame = driver.find_element(By.CLASS_NAME, 'style_card__2S1Fj')
                                                    id = frame.find_element(By.CLASS_NAME, 'style_inline__1ldLZ')
                                                    db_info['id'] = id.text
                                                    break
                                                except:
                                                    pass
                                                sleep(1)

                                            with open('_db.json', 'w') as fp:
                                                json.dump(db_info, fp)

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
                        driver.find_element(By.CLASS_NAME, 'style_noSupportBox__xumXv')
                        with open('_store.json', 'w') as fp:
                            json.dump('there are no matching players', fp)
                        print('search result count : 0')
                        print('there are no matching players')
                        break
                    except:
                        pass
                    sleep(1)

        if str(result) == 'history':
            with open('_status.json', 'r') as fp:
                status_array = json.load(fp)
            driver.get(history_url)
            while True:
                try:
                    frames = driver.find_elements(By.CLASS_NAME, 'style_card__2S1Fj')
                    for frame in frames:
                        id = frame.find_element(By.CLASS_NAME, 'style_inline__1ldLZ')
                        status = frame.find_element(By.CLASS_NAME, 'style_betStatus__nmFXN')
                        for index in status_array:
                            if str(index['bookie']) != 'PINNACLE':
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