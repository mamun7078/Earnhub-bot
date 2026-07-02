import asyncio
import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiohttp import web
import os

# --- Configuration ---
TOKEN = "8999995874:AAFli7zK13A-HtcMAiLBV-gJrCL5tktumC4"
FIREBASE_URL = "https://earning-hub-9ffec-default-rtdb.firebaseio.com"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- Start Command & Referral Handler ---
@dp.message(CommandStart())
async def start(message: Message):
    user_id = str(message.from_user.id)
    username = message.from_user.username or "User"
    
    # ইউজার লিংকে ক্লিক করলে রেফারেল আইডি বের করা (যেমন: /start 12345 থেকে 12345)
    parts = message.text.split(" ")
    ref_id = parts[1] if len(parts) > 1 else None

    # ফায়ারবেসে ডাটা চেক এবং সেভ করা
    async with aiohttp.ClientSession() as session:
        user_url = f"{FIREBASE_URL}/users/{user_id}.json"
        
        # চেক করছি ইউজার আগে থেকেই ডাটাবেসে আছে কি না
        async with session.get(user_url) as resp:
            data = await resp.json()
            
            # যদি নতুন ইউজার হয়, তবেই ডাটাবেসে সেভ করবে
            if data is None:
                new_user_data = {
                    "currentActiveLevel": "Level 1",
                    "pendingLevel": "Level 1",
                    "accountBalance": 0.00,
                    "isAccountActive": False,
                    "adsWatched": 0,
                    "lastAdDate": "",
                    "todayEarn": 0.00,
                    "todayEarnDate": "",
                    "totalRefIncome": 0.00,
                    "joinedTimestamp": 0,
                    "rewardGiven": False,
                    "username": f"@{username}"
                }
                
                # যদি রেফারেল লিংক দিয়ে আসে এবং নিজের লিংক নিজে না হয়
                if ref_id and ref_id != user_id:
                    new_user_data["referredBy"] = ref_id
                
                # ফায়ারবেসে নতুন ইউজার আপলোড করা
                await session.put(user_url, json=new_user_data)

    # ওয়েলকাম মেসেজ
    await message.answer(
        "🔥 Welcome to EarnHub!\n\n"
        "Click the 'Open' button at the bottom left to open your dashboard."
    )

# --- সার্ভার সজাগ রাখার ডামি ওয়েব সার্ভার ---
async def handle(request):
    return web.Response(text="EarnHub Bot is perfectly running 24/7!")

async def main():
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
