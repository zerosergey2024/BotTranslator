import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import TOKEN

dp = Dispatcher()
bot = Bot(token=TOKEN)


# Команда /start
@dp.message(Command('start'))
async def start(message: Message):
    await message.answer("Приветики, я бот! Используйте /dynamic для теста динамической клавиатуры.")


# Команда /dynamic
@dp.message(Command('dynamic'))
async def send_dynamic_keyboard(message: Message):
    # Создаем инлайн-кнопку "Показать больше"
    button_more = InlineKeyboardButton(text="Показать больше", callback_data="show_more")

    # Создаем инлайн-клавиатуру и добавляем кнопку
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_more]])

    # Отправляем сообщение с инлайн-кнопкой
    await message.answer("Нажмите на кнопку, чтобы показать больше опций:", reply_markup=inline_keyboard)


# Обработка нажатия на кнопку "Показать больше"
@dp.callback_query(lambda c: c.data == "show_more")
async def show_more_options(callback_query: CallbackQuery):
    # Создаем две новые инлайн-кнопки "Опция 1" и "Опция 2"
    button_option1 = InlineKeyboardButton(text="Опция 1", callback_data="option_1")
    button_option2 = InlineKeyboardButton(text="Опция 2", callback_data="option_2")

    # Обновляем клавиатуру с новыми кнопками
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_option1], [button_option2]])

    # Редактируем предыдущее сообщение, заменяя кнопку "Показать больше" на две новые кнопки
    await callback_query.message.edit_reply_markup(reply_markup=inline_keyboard)


# Обработка нажатия на кнопку "Опция 1" или "Опция 2"
@dp.callback_query(lambda c: c.data in ["option_1", "option_2"])
async def process_option(callback_query: CallbackQuery):
    # Определяем текст, который будет отправлен в зависимости от нажатой кнопки
    selected_option = "Опция 1" if callback_query.data == "option_1" else "Опция 2"

    # Отправляем сообщение с выбранной опцией
    await callback_query.message.answer(f"Вы выбрали {selected_option}")


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
