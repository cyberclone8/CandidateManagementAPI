import aioredis
import uuid
from typing import Optional

REDIS_URL = "redis://redis"

async def acquire_lock(client: aioredis.Redis, lock_key: str, ttl: int = 30) -> Optional[str]:
    lock_value = str(uuid.uuid4())
    was_set = await client.set(lock_key, lock_value, ex=ttl, nx=True)
    return lock_value if was_set else None

async def release_lock(client: aioredis.Redis, lock_key: str, lock_value: str):
    current_value = await client.get(lock_key)
    if current_value and current_value.decode() == lock_value:
        await client.delete(lock_key)