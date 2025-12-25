import motor.motor_asyncio

class DBHandler:
    def __init__(self, uri):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self.client.HackerAI_DB
        self.users = self.db.users

    async def get_user_plan(self, user_id):
        user = await self.users.find_one({"user_id": user_id})
        if not user:
            await self.users.insert_one({"user_id": user_id, "plan": "FREE", "points": 0})
            return "FREE"
        return user['plan']

    async def update_plan(self, user_id, new_plan):
        await self.users.update_one({"user_id": user_id}, {"$set": {"plan": new_plan}})
