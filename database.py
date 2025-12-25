# database.py

import os
import motor.motor_asyncio


class DBHandler:
    def __init__(self, uri: str | None = None):
        # Read from environment if not passed
        self.uri = uri or os.getenv("MONGO_URI")
        if not self.uri:
            raise ValueError("MONGO_URI is not set")

        self.client = motor.motor_asyncio.AsyncIOMotorClient(self.uri)

        # Database & collections
        self.db = self.client["HackerAI_DB"]
        self.users = self.db["users"]

    async def init_indexes(self):
        # Ensure unique user_id
        await self.users.create_index("user_id", unique=True)

    async def get_user_plan(self, user_id: int) -> str:
        user = await self.users.find_one({"user_id": user_id})
        if not user:
            await self.users.insert_one(
                {
                    "user_id": user_id,
                    "plan": "FREE",
                    "points": 0,
                    "created_at": None,
                }
            )
            return "FREE"
        return user.get("plan", "FREE")

    async def update_plan(self, user_id: int, new_plan: str):
        await self.users.update_one(
            {"user_id": user_id},
            {"$set": {"plan": new_plan}},
            upsert=True,
        )

    async def add_points(self, user_id: int, points: int):
        await self.users.update_one(
            {"user_id": user_id},
            {"$inc": {"points": points}},
            upsert=True,
        )

    async def get_points(self, user_id: int) -> int:
        user = await self.users.find_one({"user_id": user_id})
        if not user:
            return 0
        return user.get("points", 0)
