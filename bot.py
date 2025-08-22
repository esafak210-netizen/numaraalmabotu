import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart
import os

# Bot Tokeni (Heroku config vars kısmına ekleyeceğiz)
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_command(message: types.Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Numaramı paylaş", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer("Merhaba! Numaranı paylaşmak için butona bas 👇", reply_markup=kb)

@dp.message(lambda msg: msg.contact is not None)
async def get_contact(message: types.Message):
    phone = message.contact.phone_number
    user = message.from_user.full_name

    # Numarayı logla (Heroku logs üzerinden görebilirsin)
    print(f"{user} numarasını paylaştı: {phone}")

    # Kullanıcıya bilgi ver
    await message.answer("✅ Numaran alındı, teşekkürler!")

    # Kullanıcının gönderdiği mesajı sil
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except Exception as e:
        print("Mesaj silinemedi:", e)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
