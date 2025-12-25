import motor.motor_asyncio
from datetime import datetime

class DBHandler:
    def __init__(self, uri):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self.client.TelegramAI
        self.users = self.db.users

    async def get_user(self, user_id):
        user = await self.users.find_one({"user_id": user_id})
        if not user:
            user = {
                "user_id": user_id,
                "plan": "FREE",
                "points": 0,
                "expires_at": None,
                "created_at": datetime.utcnow()
            }
            await self.users.insert_one(user)
        return user

    async def update_plan(self, user_id, plan, expiry):
        await self.users.update_one(
            {"user_id": user_id},
            {"$set": {"plan": plan, "expires_at": expiry}}
        )

    async def add_points(self, user_id, points):
        await self.users.update_one(
            {"user_id": user_id},
            {"$inc": {"points": points}}
        )

    async def all_users(self):
        return await self.users.find().to_list(length=1000)
