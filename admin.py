from telethon import events
from plans import calculate_expiry

def admin_handlers(bot, db, OWNER_ID):

    @bot.on(events.NewMessage(pattern="/addplan"))
    async def add_plan(event):
        if event.sender_id != OWNER_ID:
            return

        _, user_id, plan = event.text.split()
        expiry = calculate_expiry(plan.upper())
        await db.update_plan(int(user_id), plan.upper(), expiry)
        await event.reply(f"✅ Plan {plan} added to {user_id}")

    @bot.on(events.NewMessage(pattern="/planusers"))
    async def plan_users(event):
        if event.sender_id != OWNER_ID:
            return

        users = await db.all_users()
        msg = "\n".join([f"{u['user_id']} → {u['plan']}" for u in users])
        await event.reply(msg or "No users")
