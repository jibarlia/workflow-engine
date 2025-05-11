class FakeRedis:
    def __init__(self):
        self.store = {}

    async def hset(self, key, *args, **kwargs):
        if args and len(args) == 2:
            self.store.setdefault(key, {})[args[0]] = args[1]
        elif kwargs.get("mapping"):
            self.store[key] = kwargs["mapping"]

    async def hgetall(self, key):
        return self.store.get(key, {})
    
    def get_client(self):
        return self 