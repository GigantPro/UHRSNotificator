import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from threading import Thread
from all_keys import ACCAUNTS, ADMINS

import time


driver = None
options = None

all_names = []
results = []

def start(bot):
    while True:
        all_names.clear()
        results.clear()
        thr = []
        for i in ACCAUNTS:
            thr.append(Thread(target=check_apd, args=(bot, i[0], i[1])))
            thr[-1].start()
        
        for i in thr:
            i.join()
        js = json_read(file_name='data_of_tasks.json')
        for j in results:
            for x in json_read(file_name='users.json') + [[i] for i in ADMINS]:
                if j not in js:
                    try:
                        bot.send_message(x[0], '\n'.join(j), parse_mode="Markdown")
                    except:
                        for a in ADMINS:
                            try:
                                bot.send_message(a[0], f'*Я не могу отправить {x[1]} т.к. он либо очистил чат со мной, либо заблокировал меня*', parse_mode="Markdown")
                            except:
                                print('ERROR SEND TO ADMIN:', x[0])
        json_write(results, file_name='data_of_tasks.json')
        time.sleep(200)        

def json_read(file_name = 'data_of_tasks.json'):
        with open(file_name, 'r', encoding='ASCII') as file:
            data = json.load(file)
            return data


def json_write(base, file_name = 'data_of_tasks.json'):
    with open(file_name, 'w', encoding='ASCII') as file:
        json.dump(base, file, indent=2, ensure_ascii=True)

async def send_msg(bot, id, msg):
    await bot.send_message(int(id), str(msg), parse_mode="Markdown") 

def check_apd(bot, login: str, passwd: str):
    driver = None
    options = webdriver.ChromeOptions()
    options.headless = False
    options.add_argument("--disable-blink-features=AutomationControlled")
    while True:
        try:
            print('Browser start')
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            driver.get("https://prod.uhrs.playmsn.com/")
            driver.find_element_by_id('id__0').click()
            time.sleep(2)
            email_input = driver.find_element_by_id("i0116")
            email_input.clear()
            email_input.send_keys(login)
            driver.find_element_by_id("idSIButton9").click()
            time.sleep(2)
            pass_input = driver.find_element_by_name("passwd")
            pass_input.clear()
            time.sleep(2)
            pass_input.send_keys(str(passwd))
            time.sleep(2)
            driver.find_element_by_id("idSIButton9").click()
            time.sleep(2)
            driver.find_element_by_id("idSIButton9").click()
            time.sleep(2)
            driver.get("https://prod.uhrs.playmsn.com/marketplace/tasks/all")
            time.sleep(5)
            task_card = driver.find_elements_by_class_name("task-card")
            print('task_cards in', login, ':', len(task_card))
            count_lose = 0
            for i in task_card:
                temp = str(i.text).split('\n')
                temp2 = temp[temp.index('\uedff') + 2]
                if temp2 == "\ue946":
                    temp2 = temp[temp.index('\uedff') + 3]
                try:
                    if float(temp2.split()[0][1:]) <= 10.0:
                        count_lose += 1
                        continue
                except:
                    print(end='')
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
                mass.append(temp[temp.index('\uedff') + 1])
                mass.append(temp2)
                if temp2[0] == '0':
                    continue
                if not(name in all_names):
                    results.append(mass)
                    all_names.append(name)
            driver.close()
            driver.quit()
            print("lose", count_lose)
            break
        except Exception as ex:
            driver.close()
            driver.quit()
            print(ex)
            continue
    # js = json_read()
    # if js == all_jobs:
    #     print('Browser close')
    #     time.sleep(300)
    # else:
    #     new_jobs = []
    #     for i in all_jobs:
    #         if not(i in js):
    #             new_jobs.append(i)
    #     if new_jobs:
    #         subscr = json_read(file_name='users.json')
    #         for i in subscr:
    #             for j in new_jobs:
    #                 try:
    #                     bot.send_message(i[0], '\n'.join(j), parse_mode="Markdown")
    #                 except:
    #                     continue
    #         json_write(all_jobs)
    #         json_write(all_kards, file_name='all_kards.json')
    #         print('Browser close')
    #         time.sleep(300)
    #     else:
    #         driver.close()
    #         driver.quit()
    #         print('Browser close')
    #         time.sleep(300)
