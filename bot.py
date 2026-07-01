import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiohttp import web
import os

# --- Configuration ---
TOKEN = "8999995874:AAFli7zK13A-HtcMAiLBV-gJrCL5tktumC4"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "🔥 Welcome to EarnHub!\n\n"
        "Click the 'Open' button at the bottom left to open your dashboard."
    )

# --- সার্ভারকে সজাগ রাখার জন্য ডামি ওয়েব সার্ভার ---
async def handle(request):
    return web.Response(text="EarnHub Bot is perfectly running 24/7!")

async def main():
    # ওয়েব সার্ভার চালু করা
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"🌐 Web server started on port {port}")
    
    print("🚀 EarnHub Bot is running smoothly...")
    await bot.delete_webhook(drop_pending_updates=True) 
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())