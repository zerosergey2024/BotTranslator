import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import sqlite3
import logging
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)


# Определяем состояния для FSM (Finite State Machine)
class Form(StatesGroup):
    name = State()
    age = State()
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


# Инициализируем базу данных
init_db()


# Обработчик команды /start
@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer("Привет! Как тебя зовут?")
    await state.set_state(Form.name)


# Обработчик состояния name
@dp.message(Form.name)
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько тебе лет?")
    await state.set_state(Form.age)


# Обработчик состояния age
@dp.message(Form.age)
async def age(message: Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    await message.answer("В каком ты классе?")
    await state.set_state(Form.grade)


# Обработчик состояния grade
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
