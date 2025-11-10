import time
from typing import Optional

class CacheItem:
    def __init__(self, value, ttl: int):
        self.value = value
        self.expire_at = time.time() + ttl

class SimpleCache:
    def __init__(self, ttl: int = 300):
        self.ttl = ttl
        self.store = {}

    def set(self, key, value):
        self.store[key] = CacheItem(value, self.ttl)

    def get(self, key) -> Optional[any]:
        item = self.store.get(key)
        if item and item.expire_at > time.time():
            return item.value
        elif item:
            del self.store[key]
        return None

cache = SimpleCache()
