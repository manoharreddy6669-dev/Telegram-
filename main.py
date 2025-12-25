import os
import asyncio
from telethon import TelegramClient, events, Button, functions, errors
from database import DBHandler
from assistant import HackerAI_Logic

# Environment Variables
API_ID = int(os.getenv("API_ID", 27482321))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")

# Initialize Clients
bot = TelegramClient('hackerai_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
db = DBHandler(MONGO_URI)
ai_core = HackerAI_Logic()

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    user_id = event.sender_id
    plan = await db.get_user_plan(user_id)
    
    buttons = [
        [Button.inline("📡 Advanced Scraper", "scrap_tool")],
        [Button.inline("➕ Member Adder", "add_tool")],
        [Button.inline("💀 HackerAI Assistant", "ai_tool")],
        [Button.inline("📈 View Plan & Limits", "plan_info")]
    ]
    
    await event.respond(
        f"**HackerAI Pentest Suite v2.0**\n\n"
        f"**Authorized User:** `{user_id}`\n"
        f"**Current Plan:** `{plan}`\n"
        f"**Security Status:** `Encrypted`",
        buttons=buttons
    )

# --- ADVANCED SCRAPER LOGIC ---
@bot.on(events.CallbackQuery(data="scrap_tool"))
async def scraper_menu(event):
    await event.edit("📡 **Advanced Scraper Mode**\nSend the link of the source group/channel:")
    
    @bot.on(events.NewMessage(from_users=event.sender_id))
    async def process_scraping(msg):
        bot.remove_event_handler(process_scraping)
        source = msg.text
        await msg.respond(f"🔍 **Scanning `{source}`...**\nThis may take a moment depending on group size.")
        
        try:
            # We use the user's personal session if integrated, or the bot session if it has access
            participants = await bot.get_participants(source, limit=100)
            count = 0
            with open(f"scraped_{msg.sender_id}.txt", "w") as f:
                for user in participants:
                    if user.username:
                        f.write(f"@{user.username}\n")
                        count += 1
            
            await msg.respond(f"✅ **Scraping Complete!**\nFound `{count}` members with usernames.\nFile saved as `scraped_{msg.sender_id}.txt`.")
        except Exception as e:
            await msg.respond(f"❌ **Auth Error:** Ensure the bot is a member of that group or use a user-session.\n`Error: {str(e)}`_")

# --- HACKERAI ASSISTANT (AI CODE HELP) ---
@bot.on(events.CallbackQuery(data="ai_tool"))
async def ai_tool(event):
    await event.edit("💀 **HackerAI Assistant Active**\nAsk me any technical question, request code snippets, or pentesting guidance:")

@bot.on(events.NewMessage)
async def ai_chat(event):
    if event.is_private and not event.text.startswith('/'):
        user_query = event.text
        # Process the query through the assistant logic
        response = await ai_core.generate_response(user_query)
        await event.respond(f"🤖 **HackerAI:**\n{response}")

# Deployment loop
print("HackerAI Pentest Bot is Online.")
bot.run_until_disconnected()
