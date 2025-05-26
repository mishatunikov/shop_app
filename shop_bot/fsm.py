from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from config import Config, load_config

config: Config = load_config()

if config.bot.redis:
    redis = Redis(host='redis', port=6379)
    storage = RedisStorage(
        redis=redis, key_builder=DefaultKeyBuilder(with_destiny=True)
    )
else:
    storage = MemoryStorage()
