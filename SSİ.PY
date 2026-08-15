import asyncio
import io
from PIL import Image
from aiogram import Bot, Dispatcher, types, F
from google import genai

TOKEN = "8375477671:AAFboXMRKN0ON0oQz1oKBA9PNC9FpzxmaDM"
GEMINI_API_KEY = "AQ.Ab8RN6KiiWhvdemC2TP-7yrF5jaNmqMTAVZ_eq8n3AhpfPcciw"

bot = Bot(token=TOKEN)
dp = Dispatcher()
client = genai.Client(api_key=GEMINI_API_KEY)

@dp.message(F.text == "/start")
async def cmd_start(message: types.Message):
    await message.answer(
        "Салом! Ман боти пешрафтаи шумо ҳастам. 🚀\n\n"
        "Ман метавонам ба саволҳои шумо ҷавоб диҳам ва расмҳоро таҳлил кунам!"
    )

@dp.message(F.photo)
async def handle_photo(message: types.Message):
    await message.answer("Сурат қабул шуд, онро таҳлил карда истодаам... ⏳")
    try:
        photo = message.photo[-1]
        file = await bot.get_file(photo.file_id)
        file_bytes = await bot.download_file(file.file_path)
        
        image = Image.open(io.BytesIO(file_bytes.read()))
        prompt = message.caption or "Ин сурат чиро нишон медиҳад? Муфассал шарҳ диҳед."

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt, image],
        )
        await message.answer(response.text)
    except Exception as e:
        await message.answer(f"Хатогӣ ҳангоми кор бо расм: {e}")

@dp.message(F.text)
async def handle_message(message: types.Message):
    user_text = message.text or ""
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_text,
        )
        await message.answer(response.text)
    except Exception as e:
        await message.answer(f"Хатогӣ: {e}")

async def main():
    print("Бот фаъол шуд ва ба таври худкор кор мекунад...")
    await bot.delete_webhook(drop_pending_updates=True)
    
    while True:
        try:
            await dp.start_polling(bot)
        except Exception as e:
            print(f"Хатогии шабака: {e}. Аз нав пайвастшавӣ пас аз 5 сония...")
            await asyncio.sleep(5)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот қатъ карда шуд.")
