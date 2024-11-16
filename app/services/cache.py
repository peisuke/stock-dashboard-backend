import os
import json
import redis.asyncio as redis
from typing import Optional
from upstash_redis.asyncio import Redis

# Upstash Redis の接続設定
UPSTASH_URL = os.getenv("UPSTASH_URL", "redis://localhost:6379")
UPSTASH_TOKEN = os.getenv("UPSTASH_TOKEN", "******")

redis_client = Redis(url=UPSTASH_URL, token=UPSTASH_TOKEN)

async def set_cache(key: str, value: dict, ttl: int = 3600) -> None:
    """
    Redisにデータをキャッシュする
    """
    try:
        value_json = json.dumps(value)
        await redis_client.set(key, value_json, ex=ttl)
    except Exception as e:
        raise RuntimeError(f"Failed to set cache for key {key}: {str(e)}")

async def get_cache(key: str) -> Optional[dict]:
    """
    Redisからキャッシュを取得する
    """
    try:
        data = await redis_client.get(key)
        if data:
            return json.loads(data)
        return None
    except Exception as e:
        raise RuntimeError(f"Failed to get cache for key {key}: {str(e)}")

async def delete_cache(key: str) -> None:
    """
    Redisキャッシュを削除する
    """
    try:
        await redis_client.delete(key)
    except Exception as e:
        raise RuntimeError(f"Failed to delete cache for key {key}: {str(e)}")

