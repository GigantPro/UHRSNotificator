import asyncio
from time import time
import types
from threading import Thread
from random import randint

import string
import secrets

import telebot
from telebot import types

from all_keys import TOKEN
from main_pars import check_apd, json_read, json_write


bot = telebot.TeleBot(TOKEN)

#loop = asyncio.get_event_loop()

# task_maneger_start = Thread(target=check_apd, args=(bot, loop))
# task_maneger_start.start()

admins_id = [1041024979]

create_tokens_ls = []   # {'id': ID, 'time': TIME_MINUTS}


def create_token_func(message: telebot.types.Message, skip=False, msg=None):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Установить срок')
    item2 = types.KeyboardButton('Сгенерировать')

    markup.add(item1, item2)

    if not skip:
        bot.send_message(message.chat.id, 'Привет, {0.first_name}!'.format(message.from_user) + '\nКакой ключ создадим?', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, msg, reply_markup=markup)

    all_id = []
    for i in create_tokens_ls:
        all_id.append(i['id'])
    num = 9999999999999999999
    for i in range(len(all_id)):
        if all_id[i] == message.from_user.id:
            num = i
            break
    if num == 9999999999999999999:
        create_tokens_ls.append({'id': message.from_user.id, 'time': 0})

def continue_create_token_func(message: telebot.types.Message):
    if message.text == 'Установить срок':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('1 день')
        item2 = types.KeyboardButton('1 неделя')
        item3 = types.KeyboardButton('1 месяц')
        markup.add(item1, item2, item3)
        bot.send_message(message.chat.id, 'На какой срок?', reply_markup=markup)
    elif message.text == '1 день':
        all_id = []
        for i in create_tokens_ls:
            all_id.append(i['id'])
        num = 0
        for i in range(len(all_id)):
            if all_id[i] == message.from_user.id:
                num = i
                break
        now = create_tokens_ls[num].get('time', 0) + 1440
        create_tokens_ls[num]['time'] = now
        create_token_func(message)
    elif message.text == '1 неделя':
        all_id = []
        for i in create_tokens_ls:
            all_id.append(i['id'])
        num = 0
        for i in range(len(all_id)):
            if all_id[i] == message.from_user.id:
                num = i
                break
        now = create_tokens_ls[num].get('time', 0) + 10080
        create_tokens_ls[num]['time'] = now
        create_token_func(message)
    elif message.text == '1 месяц':
        all_id = []
        for i in create_tokens_ls:
            all_id.append(i['id'])
        num = 0
        for i in range(len(all_id)):
            if all_id[i] == message.from_user.id:
                num = i
                break
        now = create_tokens_ls[num].get('time', 0) + 312480
        create_tokens_ls[num]['time'] = now
        create_token_func(message)
    elif message.text == 'Сгенерировать':
        length = randint(8, 13)
        letters_and_digits = string.ascii_letters + string.digits
        crypt_rand_string = ''.join(secrets.choice(
            letters_and_digits) for i in range(length))
        num = 999999999
        for i in range(len(create_tokens_ls)):
            if create_tokens_ls[i]['id'] == message.from_user.id:
                num = i
                break
        time = None
        if num == 999999999:
            time = None
        else:
            time = create_tokens_ls[num].get('time', None)
        if time:
            bot.send_message(message.chat.id, f'Вот сгенерированный ключ на {time} минут.')
            bot.send_message(message.chat.id, crypt_rand_string, reply_markup=types.ReplyKeyboardRemove())
            create_tokens_ls.remove(create_tokens_ls[num])
        else:
            create_token_func(message, skip=True, msg='Вы не указали время.')
            return
        json_write(json_read('tokens.json') + [[crypt_rand_string, time]], file_name='tokens.json')

def subsc(message: telebot.types.Message):
    if len(message.text.split()) > 2 or len(message.text.split()) <= 1:
        bot.send_message(message.chat.id, f'Некорректный ввод, либо неправильный токен.')
        return
    token = message.text.split()[1]
    js = json_read('tokens.json')
    temp = None
    for i in js:
        if i[0] == token:
            temp = i
            break
    if not temp:
        bot.send_message(message.chat.id, f'Некорректный ввод, либо неправильный токен.')
        return
    ttp = json_read('tokens.json').remove(temp)
    if not ttp:
        ttp = []
    json_write(ttp, file_name='tokens.json')
    js = json_read('users.json')
    tp = None
    for i in js:
        if i[0] == message.from_user.id:
            tp = i
            break
    if tp:
        js.remove(tp)
        js.append([tp[0], tp[1], tp[2] + temp[1]])
        json_write(js, file_name='users.json')
    else:
        json_write(json_read('users.json') + [[message.from_user.id, message.from_user.full_name, temp[1]]], file_name='users.json')
    bot.send_message(message.from_user.id, f'Вы активировали токен доступа на {temp[1]} минут!')

def admin(message:telebot.types.Message):
    if message.text == '/admin':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Показать всех пользователей')
        item2 = types.KeyboardButton('Закрыть')
        markup.add(item1, item2)
        bot.send_message(message.chat.id, 'Что поделаем?', reply_markup=markup)
    elif message.text == 'Показать всех пользователей':
        for i in json_read('users.json'):
            bot.send_message(message.from_user.id, f'*ID:* {i[0]}\n*Name:* {i[1]}\n*Time:* {i[2]}', parse_mode="Markdown")
    elif message.text == 'Закрыть':
        bot.send_message(message.chat.id, 'Удачи :)', reply_markup=types.ReplyKeyboardRemove())

def remove(message: types.Message):
    if not message.text.split()[1].isdigit():
        bot.send_message(message.chat.id, 'Некорректный ID')
    js = json_read('users.json')
    for i in js:
        if i[0] == int(message.text.split()[-1]):
            js.remove(i)
            json_write(js, file_name='users.json')
            bot.send_message(message.chat.id, f'Вы забрали доступ к боту у {i[1]}.\nДумаю, что он расстроится(')
            return
    bot.send_message(message.chat.id, f'У меня в базе нету такого пользователя.')

@bot.message_handler()
def echo_sent(message):
    if message.text in ['Установить срок', 'Сгенерировать', '1 день', '1 неделя', '1 месяц']:
        continue_create_token_func(message)
    elif message.text.split()[0] == '/sub':
        subsc(message)
    elif message.text == '/all':
        for i in json_write(file_name='data_of_tasks.json'):
            bot.send_message(message.chat.id, '\n'.join(i), parse_mode="Markdown")
    elif message.text == '/create' and message.from_user.id in admins_id:
        create_token_func(message)
    elif message.text in ['/admin', 'Показать всех пользователей', 'Закрыть']:
        admin(message)
    elif message.text.split()[0] == '/rem':
        remove(message)
    else:
        if message.from_user.id in json_read(file_name='subscr.json'):
            bot.send_message(message.chat.id, "вы уже подписались на рассылку.")
            return
        json_write(json_read(file_name='subscr.json') + [message.from_user.id], file_name='subscr.json')
        bot.send_message(message.chat.id, "вы подписались на рассылку.")



bot.polling(none_stop=True)
