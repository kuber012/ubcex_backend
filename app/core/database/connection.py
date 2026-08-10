from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.config import settings
from app.core.logger import logger
from app.models.domain import User, Video, Category, Subscription, Payment, Ad, Setting

db_client = None

async def init_db():
    global db_client
    logger.info("Initializing MongoDB Atlas connection...")
    try:
        db_client = AsyncIOMotorClient(settings.MONGODB_URL)
        database = db_client[settings.DATABASE_NAME]

        await init_beanie(
            database=database,
            document_models=[
                User, Video, Category, Subscription, Payment, Ad, Setting
            ]
        )

        logger.info("Database initialized and indexed successfully.")
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise e
