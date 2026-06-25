import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI") or os.getenv("MONGODB_URI") or "mongodb://localhost:27017"

class Database:
    client: AsyncIOMotorClient = None

db = Database()

def get_database():
    return db.client["edtech_db"]

async def connect_to_mongo():
    db.client = AsyncIOMotorClient(MONGO_URI)
    print("Connected to MongoDB")

async def close_mongo_connection():
    db.client.close()
    print("Closed MongoDB connection")
