from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.memory import MemoryStorage
from redis.asyncio import Redis
from aiogram.fsm.storage.redis import RedisStorage

from config import load_config, Config

config: Config = load_config()

if config.bot.redis:
    redis = Redis(host='redis', port=6379)
    storage = RedisStorage(
        redis=redis, key_builder=DefaultKeyBuilder(with_destiny=True)
    )
else:
    storage = MemoryStorage()
