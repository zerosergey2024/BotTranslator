import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import TOKEN

dp = Dispatcher()
bot = Bot(token=TOKEN)


# Команда /start
@dp.message(CommandStart())
async def start(message: Message):
    # Создаем кнопки
    button_hello = types.KeyboardButton(text="Привет")
    button_bye = types.KeyboardButton(text="Пока")

    # Создаем клавиатуру и добавляем кнопки
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[[button_hello, button_bye]],
        resize_keyboard=True
    )

    # Отправляем приветственное сообщение и меню с кнопками
    await message.answer("Приветики, я бот!", reply_markup=keyboard)


# Обработка нажатия на кнопку "Привет"
@dp.message(lambda message: message.text == "Привет")
async def say_hello(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}!")


# Обработка нажатия на кнопку "Пока"
@dp.message(lambda message: message.text == "Пока")
async def say_goodbye(message: Message):
    await message.answer(f"До свидания, {message.from_user.first_name}!")


# Команда /links
@dp.message(Command('links'))
async def send_links(message: Message):
    # Создаем инлайн-кнопки с URL-ссылками
    button_news = InlineKeyboardButton(text="Новости", url="https://news.ycombinator.com/")
    button_music = InlineKeyboardButton(text="Музыка", url="https://www.spotify.com/")
    button_video = InlineKeyboardButton(text="Видео", url="https://www.youtube.com/")

    # Создаем инлайн-клавиатуру и добавляем кнопки
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_news], [button_music], [button_video]])

    # Отправляем сообщение с инлайн-кнопками
    await message.answer("Выберите категорию:", reply_markup=inline_keyboard)


# Основная функция для запуска бота
async def main():
    try:
        await dp.start_polling(bot)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError as e:
        print(f"Runtime error occurred: {e}")
