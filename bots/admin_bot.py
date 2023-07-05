import os
import logging
import asyncio

from django.http import JsonResponse
from aiogram import Bot, executor, Dispatcher, types
from dotenv import load_dotenv


load_dotenv()
logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv('ADMIN_TOKEN', default='some_key'))
chat_id = os.getenv('MY_CHAT')
dp = Dispatcher(bot)


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

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
