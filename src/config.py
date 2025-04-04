import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    REDIS_HOST = os.getenv("REDIS_HOST", "redis_notification")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    MAX_REQUESTS_PER_MINUTE = int(os.getenv("MAX_REQUESTS_PER_MINUTE", 100))
    TIME_SECONDS = int(os.getenv("TIME_SECONDS", 60))

config = Config()