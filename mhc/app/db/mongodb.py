from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
from config import MONGODB_URL

async def get_database_conn():
    return MongoClient(MONGODB_URL)

