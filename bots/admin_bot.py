import aiocron
import asyncio
import logging
import os
import requests
import json
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType
from django.http import JsonResponse
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv('ADMIN_TOKEN', default='some_key'))
chat_id = os.getenv('GROUP_ID')
dp = Dispatcher(bot)

# Файл, где хранятся заголовки новостей
NEWS_TITLES_FILE = 'news_titles.json'


def load_news_titles():
    if os.path.exists(NEWS_TITLES_FILE):
        with open(NEWS_TITLES_FILE, 'r') as file:
            try:
                news_titles = json.load(file)
            except json.JSONDecodeError:
                news_titles = []
    else:
        news_titles = []
    return news_titles


def save_news_titles(news_titles):
    with open(NEWS_TITLES_FILE, 'w') as file:
        json.dump(news_titles, file)


def parser():
    url = 'https://fisherjournal.xyz'

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    post = soup.find(class_='col-md-6 big-post')

    title = post.find(class_='card-title').text.strip()
    url_news = post.find('a')['href'].strip()
    img = post.find('img')['src'].strip()
    group = post.find(class_='card-group').text.strip()

    news_titles = load_news_titles()

    if title in news_titles:
        print('Новость уже есть')
        return None
    else:
        news_titles.append(title)
        save_news_titles(news_titles)
        return {
            'img': img,
            'group': group,
            'title': title,
            'url': url + url_news,
        }


@dp.message_handler(
    content_types=[ContentType.NEW_CHAT_MEMBERS, ContentType.LEFT_CHAT_MEMBER]
)
async def delete_service_messages(message: types.Message):
    await bot.delete_message(
        chat_id=message.chat.id, message_id=message.message_id
    )


@aiocron.crontab('0 14 * * *')
async def send_news():
    while True:
        news = parser()
        if news:
            await bot.send_photo(
                chat_id=chat_id,
                photo=news['img'],
                caption=f"{news['title']}\n{news['url']}"
            )
        await asyncio.sleep(60 * 60)


async def send_message_to_chat(message: types.Message):
    await message.answer(message)


async def send_message_to_bot(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        username = request.POST.get('username')

        # Формируем текст сообщения
        text = (f'Имя: {name}\nEmail: {email}\nСообщение: {message}\n'
                f'Telegram: {username}')

        # Отправляем сообщение в личку
        asyncio.create_task(send_message_to_chat(text))

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'})


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
