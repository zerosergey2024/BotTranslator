import asyncio
from aiogram import Bot, Dispatcher
from aiohttp import web, ClientSession
from PIL import Image
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
import io
import random
import tempfile
import os
from config import TOKEN, NASA_API_KEY, ROVER_URL

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def validate_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    return image.width >= 1024 and image.height >= 1024 and image.mode != 'L'

async def get_mars_image_url_from_nasa():
    while True:
        sol = random.randint(0, 1722)
        params = {'sol': sol, 'api_key': NASA_API_KEY}
        async with ClientSession() as session:
            async with session.get(ROVER_URL, params=params) as resp:
                resp_dict = await resp.json()
        if 'photos' not in resp_dict:
            raise Exception
        photos = resp_dict['photos']
        if not photos:
            continue
        return random.choice(photos)['img_src']

async def get_mars_photo_bytes():
    while True:
        image_url = await get_mars_image_url_from_nasa()
        async with ClientSession() as session:
            async with session.get(image_url) as resp:
                image_bytes = await resp.read()
        if await validate_image(image_bytes):
            break
    return image_bytes

async def get_mars_photo(request):
    image = await get_mars_photo_bytes()
    return web.Response(body=image, content_type='image/jpeg')

@dp.message(Command("random_ROVER"))
async def random_ROVER(message: Message):
    image_bytes = await get_mars_photo_bytes()
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
        temp_file.write(image_bytes)
        temp_file_path = temp_file.name
    image_file = FSInputFile(temp_file_path)
    await message.answer_photo(image_file)
    # Удаление временного файла после отправки
    os.remove(temp_file_path)

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', get_mars_photo, name='mars_photo')

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '127.0.0.1', 8080)
    await site.start()

async def main():
    try:
        await asyncio.gather(
            dp.start_polling(bot),
            start_web_server()
        )
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError as e:
        print(f"Runtime error occurred: {e}")




