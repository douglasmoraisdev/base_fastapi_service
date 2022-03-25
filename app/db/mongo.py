import motor.motor_asyncio
from app.core.config import MONGODB_URL

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)

database = client.swissre_db

dominios_collection = database.get_collection("dominios_collection")
payload_collection = database.get_collection("payload_collection")