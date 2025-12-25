# main.py

import os
import asyncio
from telethon import TelegramClient, events, Button
from database import DBHandler
from assistant import HackerAI_Logic

# ================== ENV ==================
API_ID = int(os.getenv("API_ID", "27482321"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")

if not all([API_ID, API_HASH, BOT_TOKEN, MONGO_URI]):
    raise RuntimeError("Missing required environment variables")

# ================== INIT ==================
bot = TelegramClient("hackerai_bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)
db = DBHandler(MONGO_URI)
ai_core = HackerAI_Logic()

# simple per-user state (no nested handlers)
USER_STATE = {}  # user_id -> {"mode": "scrape"}

# ================== START ==================
@bot.on(events.NewMessage(pattern=r"/start"))
async def start(event):
    user_id = event.sender_id
    plan = await db.get_user_plan(user_id)

    buttons = [
        [Button.inline("📡 Advanced Scraper", b"scrap_tool")],
        [Button.inline("➕ Member Adder", b"add_tool")],
        [Button.inline("💀 HackerAI Assistant", b"ai_tool")],
        [Button.inline("📈 View Plan & Limits", b"plan_info")],
    ]

    await event.respond(
        f"**HackerAI Pentest Suite v2.0**\n\n"
        f"**User:** `{user_id}`\n"
        f"**Plan:** `{plan}`\n"
        f"**Status:** `Encrypted`",
        buttons=buttons,
    )

# ================== CALLBACKS ==================
@bot.on(events.CallbackQuery(data=b"scrap_tool"))
async def scraper_menu(event):
    USER_STATE[event.sender_id] = {"mode": "scrape"}
    await event.edit("📡 **Advanced Scraper Mode**\nSend source group/channel link:")

@bot.on(events.CallbackQuery(data=b"ai_tool"))
async def ai_tool(event):
    USER_STATE[event.sender_id] = {"mode": "ai"}
    await event.edit("💀 **HackerAI Assistant Active**\nAsk your technical question:")

# ================== MESSAGE ROUTER ==================
@bot.on(events.NewMessage)
async def router(event):
    if not event.is_private or not event.text:
        return

    user_id = event.sender_id
    state = USER_STATE.get(user_id)

    # -------- SCRAPER FLOW --------
    if state and state.get("mode") == "scrape":
        USER_STATE.pop(user_id, None)
        source = event.text.strip()
        await event.respond(f"🔍 Scanning `{source}` ...")

        try:
            participants = await bot.get_participants(source, limit=100)
            count = 0
            fname = f"scraped_{user_id}.txt"

            with open(fname, "w", encoding="utf-8") as f:
                for u in participants:
                    if u.username:
                        f.write(f"@{u.username}\n")
                        count += 1

            await event.respond(
                f"✅ **Done**\nUsers found: `{count}`",
                file=fname,
            )
        except Exception as e:
            await event.respond(f"❌ Error: `{e}`")
        return

    # -------- AI CHAT --------
    if state and state.get("mode") == "ai":
        response = await ai_core.generate_response(event.text)
        await event.respond(f"🤖 **HackerAI:**\n{response}")
        return

# ================== RUN ==================
print("HackerAI Pentest Bot is Online.")
bot.run_until_disconnected()
