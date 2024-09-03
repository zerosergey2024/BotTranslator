import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from config import TOKEN  

dp = Dispatcher()
bot = Bot(token=TOKEN)


# Команда /start
@dp.message(CommandStart())
async def start(message: Message):
    # Создаем кнопки
    button_hello = KeyboardButton(text="Привет")
    button_bye = KeyboardButton(text="Пока")

    # Создаем клавиатуру и добавляем кнопки
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[button_hello, button_bye]],  # Клавиатура ожидает список списков кнопок
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

