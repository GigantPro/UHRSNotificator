import asyncio
import aiogram
from main_pars import json_read, json_write, check_apd
from threading import Thread
from aiogram import Bot, types
from aiogram.dispatcher import dispatcher
from aiogram.utils import executor


bot = Bot(token=TOKEN)
dp = dispatcher.Dispatcher(bot)

loop = asyncio.get_event_loop()

task_maneger_start = Thread(target=check_apd, args=(bot, loop))
task_maneger_start.start()

@dp.message_handler()
async def echo_sent(message: aiogram.types.Message):
    if message.from_user.id in json_read(file_name='subscr.json'):
        await message.answer("вы уже подписались на рассылку.")
        return
    await message.answer("вы подписались на рассылку.")
    json_write(json_read(file_name='subscr.json') + [message.from_user.id], file_name='subscr.json')



executor.start_polling(dp, skip_updates=True) 
