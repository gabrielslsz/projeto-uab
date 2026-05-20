import time

class CacheService:
    _cache = {}

    @classmethod
    def get(cls, key):
        entry = cls._cache.get(key)
        if entry:
            val, expiry = entry
            if val is not None and (expiry is None or expiry > time.time()):
                return val
            else:
                cls.delete(key)
        return None

    @classmethod
    def set(cls, key, value, timeout=60):
        expiry = time.time() + timeout if timeout else None
        cls._cache[key] = (value, expiry)

    @classmethod
    def delete(cls, key):
        if key in cls._cache:
            del cls._cache[key]

    @classmethod
    def clear(cls):
        cls._cache.clear()
