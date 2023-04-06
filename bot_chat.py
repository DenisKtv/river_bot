import logging
import os
import openai

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types


load_dotenv()
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=os.getenv('CHAT_TOKEN', default='some_key'))
dp = Dispatcher(bot)
openai.api_key = os.getenv('AI_TOKEN')


async def ai(promt):
    try:
        completion = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {'role': 'system', 'content': 'Тебя зовут Ян, ты крутой рыбак '
                 'и знаешь все о рыбалке и различных спопсобах ловли рыбы'},
                {'role': 'user', 'content': promt}
            ]
        )
        return completion.choices[0].message.content
    except ConnectionError:
        return None


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply('Привет! Я эксперт в области рыбалки, что Вас '
                        'интересует?'
                        )


@dp.message_handler()
async def answer(message: types.Message):
    answer = await ai(message.text)

    if answer is not None and 'ян' in message.text.lower():
        await message.reply(answer)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
