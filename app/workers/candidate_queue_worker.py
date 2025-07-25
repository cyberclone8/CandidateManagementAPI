import asyncio
import aioredis
import json
from app.utils.redis_lock import acquire_lock, release_lock

QUEUE_NAME = "candidate:processing_queue"
RETRY_QUEUE = "candidate:retry_queue"

async def process_task(payload: dict):
    # Simulate work (e.g., resume parsing)
    print(f"Processing candidate: {payload['candidate_id']}")
    await asyncio.sleep(2)

async def worker():
    redis = aioredis.from_url("redis://redis")
    print("Worker started. Polling...")

    while True:
        task_json = await redis.lpop(QUEUE_NAME)
        if task_json:
            task = json.loads(task_json)
            lock_key = f"candidate:lock:{task['candidate_id']}"
            lock_value = await acquire_lock(redis, lock_key)

            if lock_value:
                try:
                    await process_task(task)
                except Exception as e:
                    print(f"Task failed: {e}")
                    await redis.rpush(RETRY_QUEUE, task_json)
                finally:
                    await release_lock(redis, lock_key, lock_value)
            else:
                # Re-queue for later attempt
                await redis.rpush(QUEUE_NAME, task_json)
        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(worker())