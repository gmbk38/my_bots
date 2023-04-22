import json
import requests
import pandas as pd
import numpy as np
from urllib.parse import quote
from urllib.parse import unquote
import time
import random
from ItemsNames import getItemsNames as GIN
from bs4 import BeautifulSoup
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

API_TOKEN = '6220870342:AAHwU9QScKNbsDRIpfFvVS1ojK11AOL-38g'
my_chat = -908520292

my_prc = 0.00
my_balance = 0

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# _proxies = [
#     {"http": "http://45.7.177.177:39867",
#     "https": "http://45.7.177.177:39867"},
#     {"http": "http://46.174.234.32:5678",
#     "https": "http://46.174.234.32:5678"},
#     {"http": "http://49.75.17.108:44844",
#     "https": "http://49.75.17.108:44844"},  
# ]

@dp.message_handler(commands=['data'])
async def getdata(message: types.Message):

    global my_prc
    global my_balance

    my_prc = float(message.text.split()[2])
    my_balance = int(message.text.split()[1])

    await bot.send_message(my_chat, f'Баланс: {my_balance}\nПроцент выгоды: {my_prc}')


@dp.message_handler(commands=['u3'])
async def find(message: types.Message):
    pos_counter = 0
    pos_errors = 0
    await bot.send_message(my_chat, f'Я получил задание работать с {message.text.split()[1::]}\nБаланс стим: {my_balance}\nПроцент прибыли, который вы хотите получить {my_prc}')
    for item_name in GIN(arr=message.text.split()[1::]):

        if not 'StatTrak' in item_name:
            try:
                # print('==================================================')

                # print(item_name)

                _headers = {
                    # 'Referer': url.split('#')[0],
                    'Referer': f'https://steamcommunity.com/market/listings/730/{item_name}',
                    # 'Referer': f'https://steamcommunity.com/market/search?q=&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Type%5B%5D=tag_CSGO_Type_Pistol&appid=730',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.34',

                }

                _url = f'https://steamcommunity.com/market/listings/730/{item_name}'
                _response = requests.get(_url, _headers)

                if (_response.status_code != 200):
                    print('Ошибка _url')
                    await bot.send_message(my_chat, 'Меня забанил стим, сплю 5 минут')
                    time.sleep(300)

                _soup = BeautifulSoup(_response.text, 'html.parser')
                item_id = int(str(_soup).split('Market_LoadOrderSpread')[1].split(')')[0].replace(' ','').replace('(',''))
                # print(item_id)


                suburl = f'https://steamcommunity.com/market/itemordershistogram?country=RU&language=russian&currency=5&item_nameid={item_id}&two_factor=0'

                subheaders = {
                    'Referer': f'https://steamcommunity.com/market/listings/730/{item_name}',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.34',

                    # 'If-None-Match': '"i8iZ57/JRNLQH3mKeQ6DoXjuQQw="'
                }

                subresponse = requests.get(suburl, headers=subheaders)

                if (subresponse.status_code != 200):
                    print('Ошибка suburl')
                    await bot.send_message(my_chat, 'Меня забанил стим, сплю 5 минут')
                    time.sleep(300)

                # print(subresponse)

                subsoup = subresponse.json()

                rows = subsoup['sell_order_table'].split('<td align="right" class="">')[1:6]
                prices = []
                amounts = []
                for row in rows:
                    row = row.replace('</td></tr><tr>', '').split(' pуб.</td><td align="right">')
                    prices.append(float(row[0].replace(',','.')))
                    amounts.append(int(row[1]))

                # print(prices)
                # print(amounts)

                total_price = 0
                total_amount = 0

                for i in range(0, 5):
                    total_price += prices[i]*amounts[i]
                    total_amount += amounts[i]

                mean_price = total_price/total_amount

                # print(f'Средняя цена предмета {round(mean_price, 2)}')
                # print(f'Самая низкая стоимость {prices[0]}')
                # print(mean_price, total_price, total_amount)
                # print(prices, amounts)

                max_to_buy = mean_price*(0.85-my_prc)

                if(prices[0] < max_to_buy):
                    await bot.send_message(my_chat, f'@gameboychik\n{item_name}\nМинимальная цена: {prices[0]}\nСредняя цена: {round(mean_price, 2)}\nМаксимальная цена для покупки {round(max_to_buy, 2)} с установленной выгодой {my_prc}')
                    await bot.send_message(my_chat, f'{quote(_url, safe=":/")}')
                    # print(_url)
                else:
                    # print('Не покупать')
                    pass   
                pos_counter += 1
                if (pos_counter > 15):
                    pos_counter = 0
                    await bot.send_message(my_chat, f'Я успешно проверил 15 позиций {item_name.split("|")[0]}, Допустимых ошибок {pos_errors}')
                    pos_errors = 0


                # print('==================================================\n')
            except Exception as ex:
                # print('Что-то пошло не так, но так и задумано')
                pos_errors += 1
                print(ex)
                # await bot.send_message(my_chat, f'Что-то пошло не так, но так и задумано')
                pass
        time.sleep(10)
        # 10
    time.sleep(10)

@dp.message_handler(commands=['findchat'])
async def botAnswer(message: types.Message):
    print(message.chat.id)

executor.start_polling(dp, skip_updates=True)