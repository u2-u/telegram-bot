import asyncio
import aiohttp
import json
import os
import random
import string
import time
from datetime import datetime
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.enums import ParseMode

# ===================== CONFIG =====================
# التوكن والمعرف مضافان مباشرة
BOT_TOKEN = "8768463809:AAFPa9ldzXcOiw1LGf4zpyPC7U3sWwpZqR8"
ADMIN_ID = "8190013957"

CONFIG_FILE = "tiktok_config.json"
AVAILABLE_FILE = "tiktok_available.txt"
CONCURRENCY = 25
CHECK_URL = "https://www.tiktok.com/@{}"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
]

NICE_WORDS_6 = [
    "love", "peace", "hope", "dream", "light", "smart", "happy", "lucky",
    "power", "queen", "king", "hero", "gold", "silver", "music", "dance",
    "game", "play", "free", "rich", "cool", "best", "good", "nice", "cute",
    "star", "moon", "sun", "sky", "sea", "fire", "wind", "rain", "snow",
    "blue", "red", "green", "pink", "black", "white", "sweet", "brave",
    "calm", "pure", "fast", "slow", "high", "deep", "true", "safe"
]

COMPANY_NAMES = [
    "apple", "google", "amazon", "tesla", "meta", "nvidia", "intel", "amd",
    "sony", "nike", "adidas", "samsung", "xiaomi", "huawei", "oppo", "vivo",
    "realme", "oneplus", "lenovo", "asus", "dell", "hp", "ibm", "oracle",
    "sap", "uber", "lyft", "airbnb", "netflix", "spotify", "zoom", "slack",
    "notion", "figma", "canva", "shopify", "stripe", "square", "paypal",
    "visa", "master", "twitter", "snap", "reddit", "discord", "twitch"
]

# ===================== GENERATORS =====================
def gen_1():   # #_#_#
    c = string.ascii_lowercase + string.digits
    return f"{random.choice(c)}_{random.choice(c)}_{random.choice(c)}"

def gen_2():   # #.#.#
    c = string.ascii_lowercase + string.digits
    return f"{random.choice(c)}.{random.choice(c)}.{random.choice(c)}"

def gen_3():   # #.#_#
    c = string.ascii_lowercase + string.digits
    return f"{random.choice(c)}.{random.choice(c)}_{random.choice(c)}"

def gen_4():   # ##_#.
    c = string.ascii_lowercase + string.digits
    return f"{random.choice(c)}{random.choice(c)}_{random.choice(c)}."

def gen_5():   # رباعي
    c = string.ascii_lowercase + string.digits
    return ''.join(random.choices(c, k=4))

def gen_6():   # رباعي (أحرف + أرقام)
    chars = [random.choice(string.ascii_lowercase), random.choice(string.digits),
             random.choice(string.ascii_lowercase), random.choice(string.digits)]
    random.shuffle(chars)
    return ''.join(chars)

def gen_7():   # _####
    return f"_{''.join(random.choices(string.digits, k=4))}"

def gen_8():   # ##_##
    c = string.ascii_lowercase + string.digits
    return f"{''.join(random.choices(c, k=2))}_{''.join(random.choices(c, k=2))}"

def gen_9():   # ##.##
    c = string.ascii_lowercase + string.digits
    return f"{''.join(random.choices(c, k=2))}.{''.join(random.choices(c, k=2))}"

def gen_10():  # #.#.#.#
    c = string.ascii_lowercase + string.digits
    return '.'.join(random.choices(c, k=4))

def gen_11():  # خماسي
    c = string.ascii_lowercase + string.digits
    return ''.join(random.choices(c, k=5))

def gen_12():  # خماسي مميز
    if random.random() > 0.5:
        ch = random.choice(string.ascii_lowercase)
        return ch * 4 + random.choice(string.ascii_lowercase + string.digits)
    else:
        ch = random.choice(string.ascii_lowercase)
        return random.choice(string.ascii_lowercase + string.digits) + ch * 4

def gen_13():  # خماسي (أحرف + أرقام)
    c = string.ascii_lowercase + string.digits
    return ''.join(random.choices(c, k=5))

def gen_14():  # سداسي
    c = string.ascii_lowercase + string.digits
    return ''.join(random.choices(c, k=6))

def gen_15():  # سداسي معنى جميل
    w = random.choice(NICE_WORDS_6)
    if len(w) < 6:
        w += random.choice(string.digits)
    if len(w) < 6:
        w += random.choice(string.digits)
    return w[:6].lower()

def gen_16():  # سباعي
    c = string.ascii_lowercase + string.digits
    return ''.join(random.choices(c, k=7))

def gen_17():  # سباعي مميز
    ch = random.choice(string.ascii_lowercase)
    return ch * 6 + random.choice(string.ascii_lowercase + string.digits)

def gen_18():  # سباعي اسم شركة
    name = random.choice(COMPANY_NAMES)
    if len(name) < 7:
        name += random.choice(string.digits)
    if len(name) < 7:
        name += random.choice(string.digits)
    return name[:7].lower()

def gen_19():  # عشوائي
    length = random.randint(4, 8)
    c = string.ascii_lowercase + string.digits + '_'
    return ''.join(random.choices(c, k=length))

GENERATORS = {
    1: gen_1, 2: gen_2, 3: gen_3, 4: gen_4, 5: gen_5,
    6: gen_6, 7: gen_7, 8: gen_8, 9: gen_9, 10: gen_10,
    11: gen_11, 12: gen_12, 13: gen_13, 14: gen_14, 15: gen_15,
    16: gen_16, 17: gen_17, 18: gen_18, 19: gen_19,
}

PATTERN_NAMES = {
    1: "شبه ثلاثي (#_#_#)", 2: "شبه ثلاثي (#.#.#)", 3: "شبه ثلاثي (#.#_#)",
    4: "شبه ثلاثي (##_#.)", 5: "رباعي", 6: "رباعي (أحرف+أرقام)",
    7: "شبه رباعي (_####)", 8: "شبه رباعي (##_##)", 9: "شبه رباعي (##.##)",
    10: "شبه رباعي (#.#.#.#)", 11: "خماسي", 12: "خماسي مميز",
    13: "خماسي (أحرف+أرقام)", 14: "سداسي", 15: "سداسي معنى جميل",
    16: "سباعي", 17: "سباعي مميز", 18: "سباعي اسم شركة", 19: "عشوائي",
}

# ===================== STATE =====================
class ScannerState:
    def __init__(self):
        self.running = False
        self.stop_event = asyncio.Event()
        self.checked = 0
        self.available = 0
        self.taken = 0
        self.banned = 0
        self.errors = 0
        self.lock = asyncio.Lock()
        self.start_time = None
        self.session = None
        self.admin_id = ADMIN_ID  # استخدام المعرف المحدد
        self.bot = None

state = ScannerState()

# ===================== CHECKER =====================
async def check_username(username: str) -> str:
    url = CHECK_URL.format(username)
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }

    for attempt in range(3):
        try:
            async with state.session.get(
                url, headers=headers, allow_redirects=True,
                timeout=aiohttp.ClientTimeout(total=15)
            ) as resp:
                text = await resp.text()

                if resp.status == 404:
                    return "available"

                if resp.status == 200:
                    if f'"uniqueId":"{username}"' in text or f'"uniqueId": "{username}"' in text:
                        return "taken"
                    if "user-info" in text and "avatar" in text:
                        return "taken"
                    if "Couldn&#x27;t find this account" in text or "Couldn't find this account" in text:
                        return "available"
                    if "notfound" in text.lower() or "not found" in text.lower():
                        if "user" in text.lower() or "account" in text.lower():
                            return "available"
                    if len(text) < 500:
                        return "unknown"
                    if "sigiState" not in text and "SIGI_STATE" not in text and "__UNIVERSAL_DATA_FOR_REHYDRATION__" not in text:
                        return "unknown"
                    return "taken"

                if resp.status == 403:
                    if "captcha" in text.lower() or "verify" in text.lower():
                        return "blocked"
                    return "banned"

                if resp.status in (429, 503, 502, 500):
                    await asyncio.sleep(2 ** attempt)
                    continue

                return "unknown"

        except asyncio.TimeoutError:
            if attempt < 2:
                await asyncio.sleep(1)
                continue
            return "error"
        except Exception:
            if attempt < 2:
                await asyncio.sleep(1)
                continue
            return "error"

    return "error"

# ===================== WORKERS =====================
async def worker(queue: asyncio.Queue):
    while not state.stop_event.is_set():
        try:
            username, pattern_id = await asyncio.wait_for(queue.get(), timeout=1.0)
        except asyncio.TimeoutError:
            continue

        result = await check_username(username)

        async with state.lock:
            state.checked += 1
            if result == "available":
                state.available += 1
            elif result == "taken":
                state.taken += 1
            elif result in ("banned", "blocked"):
                state.banned += 1
            else:
                state.errors += 1

        if result == "available":
            with open(AVAILABLE_FILE, "a", encoding="utf-8") as f:
                f.write(f"{username} | {PATTERN_NAMES[pattern_id]} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

            try:
                msg = (
                    f"🎯 *معرف متاح جديد!*\n\n"
                    f"👤 `@{username}`\n"
                    f"📋 النمط: {PATTERN_NAMES[pattern_id]}\n"
                    f"⏰ {datetime.now().strftime('%H:%M:%S')}"
                )
                await state.bot.send_message(chat_id=state.admin_id, text=msg, parse_mode=ParseMode.MARKDOWN)
            except Exception:
                pass

        queue.task_done()

async def generator_task(queue: asyncio.Queue):
    while not state.stop_event.is_set():
        pattern_id = random.randint(1, 19)
        username = GENERATORS[pattern_id]()
        if 2 <= len(username) <= 24:
            await queue.put((username, pattern_id))
        await asyncio.sleep(0.02)

async def stats_task():
    last_checked = 0
    while not state.stop_event.is_set():
        await asyncio.sleep(6)
        async with state.lock:
            checked = state.checked
            available = state.available
            taken = state.taken
            banned = state.banned
            errors = state.errors

        if checked > last_checked:
            last_checked = checked
            elapsed = time.time() - state.start_time if state.start_time else 1
            speed = checked / elapsed if elapsed > 0 else 0

            msg = (
                f"📊 *إحصائيات الفحص*\n\n"
                f"✅ تم الفحص: `{checked}`\n"
                f"🎯 متاح: `{available}`\n"
                f"❌ مستخدم: `{taken}`\n"
                f"🚫 محظور: `{banned}`\n"
                f"⚠️ غير معروف: `{errors}`\n"
                f"⚡ السرعة: `{speed:.1f}` فحص/ث"
            )
            try:
                await state.bot.send_message(chat_id=state.admin_id, text=msg, parse_mode=ParseMode.MARKDOWN)
            except Exception:
                pass

# ===================== TELEGRAM HANDLERS =====================
dp = Dispatcher()

def is_admin(user_id: int) -> bool:
    return str(user_id) == str(state.admin_id)

@dp.message(Command("start"))
async def cmd_start(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ ليس لديك صلاحية.")
        return

    if state.running:
        await message.answer("⚠️ الفحص يعمل بالفعل!")
        return

    # Reset state
    state.running = True
    state.stop_event.clear()
    state.checked = 0
    state.available = 0
    state.taken = 0
    state.banned = 0
    state.errors = 0
    state.start_time = time.time()

    connector = aiohttp.TCPConnector(limit=100, limit_per_host=50, ttl_dns_cache=300)
    state.session = aiohttp.ClientSession(connector=connector)

    queue = asyncio.Queue(maxsize=500)

    tasks = [
        asyncio.create_task(generator_task(queue)),
        *[asyncio.create_task(worker(queue)) for _ in range(CONCURRENCY)],
        asyncio.create_task(stats_task()),
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="⏹️ إيقاف الفحص", callback_data="stop")]]
    )

    await message.answer(
        "✅ *بدأ الفحص!*\n\nجاري البحث عن معرفات TikTok متاحة...",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=keyboard
    )

    # Wait until stopped
    await state.stop_event.wait()

    for t in tasks:
        t.cancel()

    try:
        await asyncio.wait_for(queue.join(), timeout=5.0)
    except asyncio.TimeoutError:
        pass

    await state.session.close()
    state.session = None
    state.running = False

    await state.bot.send_message(
        chat_id=state.admin_id,
        text="🛑 *تم إيقاف الفحص.*\n\nاستخدم /start للبدء من جديد.",
        parse_mode=ParseMode.MARKDOWN
    )

@dp.message(Command("stop"))
async def cmd_stop(message: Message):
    if not is_admin(message.from_user.id):
        return
    if not state.running:
        await message.answer("⚠️ لا يوجد فحص يعمل حالياً.")
        return
    state.stop_event.set()
    await message.answer("🛑 جاري إيقاف الفحص...")

@dp.callback_query(F.data == "stop")
async def cb_stop(callback: CallbackQuery):
    await callback.answer()
    if not is_admin(callback.from_user.id):
        await callback.message.edit_text("⛔ ليس لديك صلاحية.")
        return
    if not state.running:
        await callback.message.edit_text("⚠️ لا يوجد فحص يعمل.")
        return
    state.stop_event.set()
    await callback.message.edit_text("🛑 جاري إيقاف الفحص...")

@dp.message(Command("status"))
async def cmd_status(message: Message):
    if not is_admin(message.from_user.id):
        return
    if not state.running:
        await message.answer("⚠️ لا يوجد فحص يعمل حالياً.")
        return

    async with state.lock:
        checked = state.checked
        available = state.available
        taken = state.taken
        banned = state.banned
        errors = state.errors

    elapsed = time.time() - state.start_time if state.start_time else 1
    speed = checked / elapsed if elapsed > 0 else 0

    msg = (
        f"📊 *الحالة الحالية*\n\n"
        f"✅ تم الفحص: `{checked}`\n"
        f"🎯 متاح: `{available}`\n"
        f"❌ مستخدم: `{taken}`\n"
        f"🚫 محظور: `{banned}`\n"
        f"⚠️ غير معروف: `{errors}`\n"
        f"⚡ السرعة: `{speed:.1f}` فحص/ث"
    )
    await message.answer(msg, parse_mode=ParseMode.MARKDOWN)

# ===================== MAIN =====================
async def main():
    # إعداد البوت باستخدام التوكن المحدد
    state.bot = Bot(token=BOT_TOKEN)
    state.admin_id = ADMIN_ID

    # إنشاء ملف النتائج إذا لم يكن موجوداً
    if not os.path.exists(AVAILABLE_FILE):
        with open(AVAILABLE_FILE, "w", encoding="utf-8") as f:
            f.write("# TikTok Available Usernames\n")
            f.write(f"# Started at: {datetime.now()}\n")
            f.write("-" * 50 + "\n")

    print("=" * 50)
    print("🤖 TikTok Scanner Bot")
    print("=" * 50)
    print(f"✅ تم تشغيل البوت بنجاح!")
    print(f"👤 معرف الأدمن: {ADMIN_ID}")
    print(f"📁 ملف النتائج: {AVAILABLE_FILE}")
    print("-" * 50)
    print("📌 الأوامر المتاحة:")
    print("  /start  - بدء الفحص")
    print("  /stop   - إيقاف الفحص")
    print("  /status - عرض الإحصائيات")
    print("=" * 50)

    try:
        await dp.start_polling(state.bot, skip_updates=True)
    finally:
        await state.bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())