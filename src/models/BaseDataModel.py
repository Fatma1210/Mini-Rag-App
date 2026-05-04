from helpers.config import Settings, get_settings
from motor.motor_asyncio import AsyncIOMotorClient

class BaseDataModel:
    def __init__(self, db_client: AsyncIOMotorClient):
        self.settings: Settings = get_settings()
        self.db_client = db_client
        self.db = self.db_client[self.settings.MONGODB_DATABASE]  # ✅ access db directly