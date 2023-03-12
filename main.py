import requests
from bs4 import BeautifulSoup as bs


url = 'https://allrivers.info/gauge/pripyat-mozyr'
url2 = 'https://allrivers.info/gauge/pripyat-mozyr/weather'
url3 = 'https://allrivers.info/gauge/pripyat-mozyr/waterlevel'

r = requests.get(url)
r2 = requests.get(url2)
r3 = requests.get(url3)

soup = bs(r.text, 'lxml')
soup2 = bs(r2.text, 'lxml')
soup3 = bs(r3.text, 'lxml')

main_info_river = soup.find_all(class_='list-item')
temp_info = soup2.find_all(class_='list-item')
water_info = soup3.find_all(class_='mb-2')

change_for_day = soup3.find('p', class_='mb-2').find_all('b')
average_lvl = soup3.find_all('li', class_='pl-2')
pavodok_lvl = soup3.find_all(class_='alert-label rounded px-4 py-1 me-3')

print('УРОВНИ ПАВОДКА:')
print(
    f'{pavodok_lvl[0].text.strip()}'
    f' - критический режим повышенной готовности'
)
print(
    f'{pavodok_lvl[1].text.strip()}'
    f' - опасное явление, подтопление жилых помещений \n'
)

print('СВОДКА ИЗМЕРЕНИЙ:')
print(main_info_river[0].text.strip())
print(f'Уровень воды сегодня {change_for_day[0].text} см')
print(f'За прошедшие 24 часа уровень изменился на {change_for_day[1].text} см')
print(f'Средний уровень воды {average_lvl[1].text.partition(":")[2]}')
print(f'{main_info_river[4].text.strip()}\n')

# # print(water_info[0].text.strip())
# # print(water_info[1].text.strip())
# # print(water_info[2].text.strip())
# # print(water_info[3].text.strip())
# # print(water_info[4].text.strip())

print('ПРОГНОЗ ПОГОДЫ:')
print(temp_info[0].text.strip())
print(temp_info[1].text.strip())
print(temp_info[2].text.strip())
print(temp_info[3].text.strip())
print(temp_info[4].text.strip())
