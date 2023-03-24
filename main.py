import requests
import os
import logging

from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
from bs4 import BeautifulSoup as bs

from data import LAKE_AND_RIVERS

load_dotenv()
# задаем уровень логов
logging.basicConfig(level=logging.INFO)
# инициализация бота
bot = Bot(token=os.getenv('TOKEN', default='some_key'))
dp = Dispatcher(bot)


@dp.message_handler()
async def user_message(message: types.Message):
    arr = []
    user_text = message.text.lower()
    if user_text in LAKE_AND_RIVERS:
        arr.append(LAKE_AND_RIVERS[user_text])
    else:
        data = 'Такой реки нет!'
        await message.answer(text=data)

    # парсим данные в зависимости от текста юзера
    for part_url in arr:
        url = f'https://allrivers.info/gauge/{part_url}'
        url2 = f'https://allrivers.info/gauge/{part_url}/weather'
        url3 = f'https://allrivers.info/gauge/{part_url}/waterlevel'

        r = requests.get(url)
        r2 = requests.get(url2)
        r3 = requests.get(url3)

        soup = bs(r.text, 'lxml')
        soup2 = bs(r2.text, 'lxml')
        soup3 = bs(r3.text, 'lxml')

        river_name = soup.find_all(class_='breadcrumb-item')
        name_river = river_name[3].text.strip()
        dot_name = river_name[4].text.strip()

        main_info_river = soup.find_all(class_='list-item')
        temp_info = soup2.find_all(class_='list-item')
        change_for_day = soup3.find('p', class_='mb-2').find_all('b')
        average_lvl = soup3.find_all('li', class_='pl-2')
        pavodok_lvl = soup3.find_all(
            class_='alert-label rounded px-4 py-1 me-3'
        )

        # выводим название реки и точки измерения
        data = (f'Название реки: {name_river},\n'
                f'Название места: {dot_name}')
        await message.answer(text=data)

        # проверяем есть ли данные об уровне паводка и выводим результат
        try:
            data_2 = (f'УРОВНИ ПАВОДКА:\n'
                      f'{pavodok_lvl[0].text.strip()}'
                      f' - критический режим повышенн`ой готовности\n'
                      f'{pavodok_lvl[1].text.strip()}'
                      f' - опасное явление, подтопление жилых помещений \n')
            await message.answer(text=data_2)
        except IndexError:
            await message.answer('данных о УРОВНЯХ ПАВОДКА временно нет\n')

        # проверяем есть ли данные о среднем уровне воды
        try:
            average = (f'Средний уровень воды'
                       f'{average_lvl[1].text.partition(":")[2]}')
        except IndexError:
            average = (f'Данных о среднем уровне реки {name_river}'
                       f' на этот день нет!')

        # выводим информацию о текущих измерениях
        data_3 = (f'СВОДКА ИЗМЕРЕНИЙ:\n'
                  f'{main_info_river[0].text.strip()}\n'
                  f'Уровень воды сегодня {change_for_day[0].text} см\n'
                  f'{average}\n'
                  f'За прошедшие 24 часа уровень изменился на'
                  f' {change_for_day[1].text}см\n'
                  f'{main_info_river[4].text.strip()}\n')
        await message.answer(text=data_3)

        # выводим данные о погоде в точке измерения
        data_4 = (f'ПРОГНОЗ ПОГОДЫ в {dot_name}\n'
                  f'{temp_info[0].text.strip()}\n'
                  f'{temp_info[1].text.strip()}\n'
                  f'{temp_info[2].text.strip()}\n'
                  f'{temp_info[3].text.strip()}\n'
                  f'{temp_info[4].text.strip()}\n')
        await message.answer(text=data_4)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
