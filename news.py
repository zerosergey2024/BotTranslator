import asyncio
import logging
import requests
from aiogram import Bot, Dispatcher,  types
from aiogram.filters import CommandStart, Command

from config import TOKEN, NEWS_API_KEY
logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message((CommandStart()))
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я могу отправить тебе последние новости. Введи тему новостей, которую ты хочешь узнать.")

@dp.message()
async def get_news(message: types.Message):
    topic = message.text
    url = f'https://newsapi.org/v2/everything?q={topic}&apiKey={NEWS_API_KEY}'
    response = requests.get(url)
    news_data = response.json()

    if news_data['status'] == 'ok':
        articles = news_data['articles']
        for article in articles[:5]:  # Отправляем только первые 5 новостей
            await message.reply(f"{article['title']}\n{article['url']}")
    else:
        await message.reply("Извините, что-то пошло не так. Попробуйте позже.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())