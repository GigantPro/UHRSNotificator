import json
from re import sub
from tracemalloc import start
from async_timeout import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time

driver = None
options = None

USER_UHRS_LOGIN = YOUR_MICROSOFT_LOGIN
USER_UHRS_PASSWORD = YPUR_MICROSOFT_PASSWORD


def json_read(file_name = 'data_of_tasks.json'):
        with open(file_name, 'r', encoding='ASCII') as file:
            data = json.load(file)
            return data


def json_write(base, file_name = 'data_of_tasks.json'):
    with open(file_name, 'w', encoding='ASCII') as file:
        json.dump(base, file, indent=2, ensure_ascii=True)

async def send_msg(bot, id, msg):
    await bot.send_message(int(id), str(msg), parse_mode="Markdown") 

def check_apd(bot, loop):
    options = webdriver.ChromeOptions()
    options.headless = False
    options.add_argument("--disable-blink-features=AutomationControlled")
    while True:
        all_jobs = []
        all_kards = []
        try:
            print('Browser start')
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            driver.get("https://prod.uhrs.playmsn.com/")
            time.sleep(3)
            log_button = driver.find_element_by_id('id__0').click()
            time.sleep(3)
            email_input = driver.find_element_by_id("i0116")
            email_input.clear()
            email_input.send_keys(USER_UHRS_LOGIN)
            time.sleep(2)
            next_but = driver.find_element_by_id("idSIButton9").click()
            time.sleep(3)
            pass_input = driver.find_element_by_id("i0118")
            pass_input.clear()
            pass_input.send_keys(USER_UHRS_PASSWORD)
            time.sleep(2)
            next_but2 = driver.find_element_by_id("idSIButton9").click()
            time.sleep(2)
            yes_but = driver.find_element_by_id("idSIButton9").click()
            time.sleep(3)
            cookies = driver.get_cookies()
            driver.get("https://prod.uhrs.playmsn.com/marketplace/tasks/all")
            time.sleep(6)
            task_card = driver.find_elements_by_class_name("task-card")
            for i in task_card:
                temp = str(i.text).split('\n')
                #['EntityCuration_Crowd', '\uedff', '0,05 $ / HIT', '~1442.6k HITs', 'Verify the business website', '4 days ago1 min / HIT', '\uf2bc', '\ue896', '\ue76e', 'Start']
                #[name, $/hit, count_hit, description, time, todo]
                name = '*'
                for j in temp:
                    if j == '\uedff':
                        break
                    name += j
                name += '*'
                mass = []
                if 'usefulness' in name.lower() or 'image' in name.lower() or 'video' in name.lower()\
                    or 'describe' in name.lower() or 'satisfaction' in name.lower() or 'side by side' in name.lower():
                    mass.append('*❗️❗️❗️Best work❗️❗️❗️*')
                mass.append(name)
                temp2 = temp[temp.index('\uedff') + 2]
                if temp2 == "\ue946":
                    temp2 = temp[temp.index('\uedff') + 3]
                mass.append(temp[temp.index('\uedff') + 1])
                mass.append(temp2)
                if temp2[0] == '0':
                    continue
                all_jobs.append(mass)
                all_kards.append(temp)
        except Exception as ex:
            print(ex)
            continue
        js = json_read()
        if js == all_jobs:
            driver.close()
            driver.quit()
            print('Browser close')
            time.sleep(300)
        else:
            new_jobs = []
            for i in all_jobs:
                if not(i in js):
                    new_jobs.append(i)
            if new_jobs:
                subscr = json_read(file_name='subscr.json')
                for i in subscr:
                    for j in new_jobs:
                        try:
                            loop.create_task(send_msg(bot, i, '\n'.join(j)))
                        except:
                            subscr.remove(i)
                            json_write(subscr, file_name='subscr.json')
                json_write(all_jobs)
                json_write(all_kards, file_name='all_kards.json')
                driver.close()
                driver.quit()
                print('Browser close')

                time.sleep(300)
            else:
                driver.close()
                driver.quit()
                print('Browser close')
                time.sleep(300)
