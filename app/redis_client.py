import redis.asyncio as redis

class RedisClient:
    def __init__(self, host="localhost", port=6379, db=0):
        self.client = redis.Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True
        )

    def get_client(self):
        return self.client