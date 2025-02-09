import redis
import os
from dotenv import load_dotenv

load_dotenv()


redis_host = os.getenv("REDIS_HOST")
redis_port = os.getenv("REDIS_PORT")


class RedisClient:
    _instance = None

    @classmethod
    def initialize(cls, host: str = "localhost", port: int = 6379, db: int = 0):
        if cls._instance is None:
            cls._instance = redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)
        return cls._instance

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            raise RuntimeError("RedisClient not initialized. Call RedisClient.initialize() first.")
        return cls._instance
