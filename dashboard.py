from fastapi import FastAPI
from database import DBHandler
import os

app = FastAPI()
db = DBHandler(os.getenv("MONGO_URI"))

@app.get("/")
async def home():
    return {"status": "Telegram AI Bot Dashboard Running"}

@app.get("/users")
async def users():
    return await db.all_users()
