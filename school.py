import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from config import TOKEN
import sqlite3
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import aiohttp
import logging

bot = Bot(token=TOKEN, )
from config import TOKEN, WEATHER_API_KEY

dp = Dispatcher()

logging.basicConfig(level=logging.INFO)


class Form(StatesGroup):
    name = State()
    age = State()
    city = State()
    grade = State()


# Функция для инициализации базы данных и создания таблицы students
def init_db():
    conn = sqlite3.connect('school_data.db')
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        grade TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()


init_db()


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer("Привет! Как тебя зовут?")
    await state.set_state(Form.name)


@dp.message(Form.name)
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько тебе лет?")
    await state.set_state(Form.age)


@dp.message(Form.age)
async def age(message: Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    await message.answer("В каком классе ты учишься?")
    await state.set_state(Form.grade)


@dp.message(Form.grade)
async def grade(message: Message, state: FSMContext):
    await state.update_data(grade=message.text)

    # Получаем данные пользователя из FSMContext
    user_data = await state.get_data()

    # Сохраняем данные в базу данных school_data.db
    conn = sqlite3.connect('school_data.db')
    cur = conn.cursor()
    cur.execute('''
    INSERT INTO students (name, age, grade) VALUES (?, ?, ?)''',
                (user_data['name'], user_data['age'], user_data['grade']))
    conn.commit()
    conn.close()

    await message.answer(f"Спасибо! Ты добавлен в базу данных:\n"
                         f"Имя: {user_data['name']}\n"
                         f"Возраст: {user_data['age']}\n"
                         f"Класс: {user_data['grade']}")
    await state.clear()  # Сбрасываем состояние FSM


# Запуск бота
if __name__ == '__main__':
    dp.run_polling(bot)
