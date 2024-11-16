import os
import aioredis

REDIS_URL = os.getenv("REDIS_URL")

redis = aioredis.from_url(REDIS_URL)

async def cache_data(key: str, value: dict, ttl: int = 3600):
    await redis.set(key, json.dumps(value), ex=ttl)

async def get_cached_data(key: str):
    data = await redis.get(key)
    if data:
        return json.loads(data)
    return None

