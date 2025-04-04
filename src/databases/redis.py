from redis import Redis
from src.config import config

redis_client = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0, decode_responses=True)