import requests
import os
import logging

from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
from datetime import datetime
from bs4 import BeautifulSoup as bs

from data import LAKE_AND_RIVERS, RIVERS_WITH_MANY_DOTS, DATA_LIST

load_dotenv()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv('TOKEN', default='some_key'))
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    """Обработка команды Старт"""
    await message.answer(
        'Введите название реки, например припять или горынь, для получения '
        'полного списка рек и озер, введите слово список'
    )


async def user_message(message):
    """Обработка входящих сообщений"""
    arr_riv = []
    all_river = ''
    all_dots = ''
    user_text = message.text.lower()
    if user_text in RIVERS_WITH_MANY_DOTS:
        arr_name = RIVERS_WITH_MANY_DOTS[user_text]
        data1 = ('У данной реки несколько точек измерения, '
                 'введите название из соответствующего списка:\n')
        for name in arr_name:
            all_dots += f'{name}\n'
        return data1 + all_dots

    elif user_text in LAKE_AND_RIVERS:
        arr_riv.append(LAKE_AND_RIVERS[user_text])
        return arr_riv

    elif user_text == 'список':
        data = (
            f'Всего данных в списке {len(DATA_LIST)}!\n'
            'Реки, озера и водохранилища находятся в АЛФАВИТНОМ ПОРЯДКЕ:\n'
        )
        for name_riv in DATA_LIST:
            all_river += f'{name_riv}\n'
        return data + all_river
    else:
        return None


async def pars_answer(answer):
    """Парсинг данных и сбор их в одну переменную"""
    url_env = os.getenv('URL')
    big_data = ''
    for part_url in answer:
        url = f'{url_env}/{part_url}'
        url2 = f'{url_env}/{part_url}/weather'
        url3 = f'{url_env}/{part_url}/waterlevel'

        r = requests.get(url)
        r2 = requests.get(url2)
        r3 = requests.get(url3)

        soup = bs(r.text, 'lxml')
        soup2 = bs(r2.text, 'lxml')
        soup3 = bs(r3.text, 'lxml')

        # парсинг общей информации
        river_name = soup.find_all(class_='breadcrumb-item')
        name_river = river_name[3].text.strip()
        dot_name = river_name[4].text.strip()
        main_info_river = soup.find_all(class_='list-item')

        # парсинг информации о реке
        changes_in_day = main_info_river[3].find('b')
        change = changes_in_day.text.strip()
        change_for_day = soup3.find('p', class_='mb-2').find_all('b')
        average_lvl = soup3.find_all('li', class_='pl-2')
        pavodok_lvl = soup3.find_all(
            class_='alert-label rounded px-4 py-1 me-3'
        )

        # парсинг информации о погоде
        time = datetime.now()
        if time.hour >= 21:
            x = 0
        else:
            x = 1

        # next day weather
        temp_info = soup2.find_all(class_='list-item')
        temp_next = soup2.find_all(class_='tempday rounded border mb-2')
        temp_next_day = temp_next[x].find_all(class_='date-title mb-3')
        temp_next_time = temp_next[x].find_all(class_='bg-blue')
        temp_next_temp = temp_next[x].find_all(class_='temperature flex-fill')
        temp_next_title = temp_next[x].find_all(
            class_='temperature-icon me-3 flex-fill'
        )
        temp_next_wind = temp_next[x].find_all(class_='wind flex-fill')
        temp_next_preasure = temp_next[x].find_all(
            class_='d-flex flex-row mb-2 justify-content-md-start '
                   'justify-content-center'
        )

        # выводим название реки и точки измерения
        data = (f'Название: {name_river},\n'
                f'Название места: {dot_name}\n')
        big_data += data + '\n'

        # проверяем есть ли данные об уровне паводка и выводим результат
        try:
            data_2 = (f'УРОВНИ ПАВОДКА:\n'
                      f'{pavodok_lvl[0].text.strip()}'
                      f' - критический режим повышенной готовности\n'
                      f'{pavodok_lvl[1].text.strip()}'
                      f' - опасное явление, подтопление жилых помещений \n')
            big_data += data_2 + '\n'
        except IndexError:
            error = 'Данные об УРОВНЯХ ПАВОДКА временно отсутствуют\n'
            big_data += error + '\n'

        # проверяем есть ли данные о среднем уровне воды
        try:
            average = (f'Средний уровень воды'
                       f'{average_lvl[1].text.partition(":")[2]}')
        except IndexError:
            average = (f'Данных о среднем уровне реки {name_river}'
                       f' на этот день нет!')
        # проверка на изминение уровня воды
        try:
            change = (f'За прошедшие 24 часа уровень изменился на'
                      f' {change[change.find("(") + 1:change.find(")")]}см\n')
        except IndexError:
            change = 'За прошедшие 24 часа уровень воды не изменился!'
        # выводим информацию о текущих измерениях
        try:
            data_3 = (f'СВОДКА ИЗМЕРЕНИЙ:\n'
                      f'{main_info_river[0].text.strip()}\n'
                      f'Уровень воды сегодня {change_for_day[0].text} см\n'
                      f'{average}\n'
                      f'{change}\n'
                      f'{main_info_river[4].text.strip()}\n')
        except IndexError:
            data_3 = ('СВОДКА ИЗМЕРЕНИЙ: временно отсутствует, пожалуйста, '
                      'попробуйте позже')
        big_data += data_3 + '\n'

        # выводим данные о погоде в точке измерения
        try:
            data_4 = (f'ПРОГНОЗ ПОГОДЫ в {dot_name} сегодня:\n'
                      f'{temp_info[0].text.strip()}\n'
                      f'{temp_info[1].text.strip()}\n'
                      f'{temp_info[2].text.strip()}\n'
                      f'{temp_info[3].text.strip()}\n'
                      f'{temp_info[4].text.strip()}\n')
        except IndexError:
            data_4 = (f'ПРОГНОЗ ПОГОДЫ в {dot_name} на сегодня временно '
                      'отсутствует, попробуйте проверить чуть позже')
        big_data += data_4 + '\n'

        # выводим данные о погоде на сл.день каждые 6 часов
        try:
            day = {temp_next_day[0].text.strip().upper()}
        except IndexError:
            day = 'Погода на завтра: '

        try:
            data_5 = (f'{day}\n'
                      f'| Время: {temp_next_time[0].text.strip()} | '
                      'Температура '
                      f'{temp_next_temp[0].text.strip()} | '
                      f'{temp_next_title[0].find("img").get("title")} | '
                      'Ветер: '
                      f'{temp_next_wind[0].text.strip()} | '
                      f'{temp_next_preasure[0].text.strip()} |\n\n'
                      f'| Время: {temp_next_time[3].text.strip()} | '
                      'Температура '
                      f'{temp_next_temp[3].text.strip()} | '
                      f'{temp_next_title[3].find("img").get("title")} | '
                      'Ветер: '
                      f'{temp_next_wind[3].text.strip()} | '
                      f'{temp_next_preasure[3].text.strip()} |\n\n'
                      f'| Время: {temp_next_time[5].text.strip()} | '
                      'Температура '
                      f'{temp_next_temp[5].text.strip()} | '
                      f'{temp_next_title[5].find("img").get("title")} | '
                      'Ветер: '
                      f'{temp_next_wind[5].text.strip()} | '
                      f'{temp_next_preasure[5].text.strip()} |\n\n'
                      f'| Время: {temp_next_time[7].text.strip()} | '
                      'Температура '
                      f'{temp_next_temp[7].text.strip()} | '
                      f'{temp_next_title[7].find("img").get("title")} | '
                      'Ветер: '
                      f'{temp_next_wind[7].text.strip()} | '
                      f'{temp_next_preasure[7].text.strip()} |\n\n')
        except IndexError:
            data_5 = ('Данные о погоде на завтра временно отсутствуют, '
                      'попробуйте проверить чуть позже')
        big_data += data_5
    return big_data


@dp.message_handler()
async def answer(message: types.Message):
    """Обработка ответа бота"""
    answer = await user_message(message)
    if answer is not None and type(answer) == list:
        ans = await pars_answer(answer)
        await message.reply(ans)
    elif answer is not None:
        await message.reply(answer)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
