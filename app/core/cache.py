# app/core/cache.py
import json
import logging
from typing import Optional, Any, Union
import redis.asyncio as redis

from app.config import settings

logger = logging.getLogger(__name__)

class Cache:
    """Redis cache wrapper"""

    def __init__(self):
        self.redis_client: Optional[redis.Redis] = None
        self.enabled = True

    async def init_cache(self):
        """Initialize Redis connection"""
        try:
            self.redis_client = redis.Redis.from_url(
                settings.REDIS_URL,
                decode_responses=True
            )
            await self.redis_client.ping()
            logger.info("Redis cache initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Redis cache: {e}")
            self.enabled = False

    async def close(self):
        """Close Redis connection"""
        if self.redis_client:
            await self.redis_client.close()

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if not self.enabled or not self.redis_client:
            return None

        try:
            value = await self.redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in cache"""
        if not self.enabled or not self.redis_client:
            return False

        try:
            json_value = json.dumps(value)
            if ttl:
                await self.redis_client.setex(key, ttl, json_value)
            else:
                await self.redis_client.set(key, json_value)
            return True
        except Exception as e:
            logger.error(f"Cache set error: {e}")
            return False

    async def delete(self, key: str) -> bool:
        """Delete value from cache"""
        if not self.enabled or not self.redis_client:
            return False

        try:
            await self.redis_client.delete(key)
            return True
        except Exception as e:
            logger.error(f"Cache delete error: {e}")
            return False

    async def exists(self, key: str) -> bool:
        """Check if key exists in cache"""
        if not self.enabled or not self.redis_client:
            return False

        try:
            return await self.redis_client.exists(key) > 0
        except Exception as e:
            logger.error(f"Cache exists error: {e}")
            return False

    async def expire(self, key: str, ttl: int) -> bool:
        """Set expiration time for key"""
        if not self.enabled or not self.redis_client:
            return False

        try:
            return await self.redis_client.expire(key, ttl)
        except Exception as e:
            logger.error(f"Cache expire error: {e}")
            return False

    async def increment(self, key: str, amount: int = 1) -> Optional[int]:
        """Increment numeric value in cache"""
        if not self.enabled or not self.redis_client:
            return None

        try:
            return await self.redis_client.incrby(key, amount)
        except Exception as e:
            logger.error(f"Cache increment error: {e}")
            return None

# Global cache instance
cache = Cache()

async def init_cache():
    """Initialize global cache"""
    await cache.init_cache()

async def close_cache():
    """Close global cache"""
    await cache.close()

# Cache key patterns
class CacheKeys:
    """Cache key constants"""

    @staticmethod
    def user_profile(user_id: int) -> str:
        return f"user:profile:{user_id}"

    @staticmethod
    def user_permissions(user_id: int) -> str:
        return f"user:permissions:{user_id}"

    @staticmethod
    def university_data(university_id: int) -> str:
        return f"university:data:{university_id}"

    @staticmethod
    def faculty_data(faculty_id: int) -> str:
        return f"faculty:data:{faculty_id}"

    @staticmethod
    def department_data(department_id: int) -> str:
        return f"department:data:{department_id}"

    @staticmethod
    def course_data(course_id: int) -> str:
        return f"course:data:{course_id}"

    @staticmethod
    def student_data(student_id: int) -> str:
        return f"student:data:{student_id}"

    @staticmethod
    def api_rate_limit(identifier: str) -> str:
        return f"rate_limit:api:{identifier}"

    @staticmethod
    def auth_attempts(identifier: str) -> str:
        return f"auth:attempts:{identifier}"

# Cache decorators
def cached(ttl: Optional[int] = None):
    """Decorator for caching function results"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Generate cache key from function name and arguments
            key = f"{func.__name__}:{str(args)}:{str(kwargs)}"

            # Try to get from cache first
            cached_result = await cache.get(key)
            if cached_result is not None:
                return cached_result

            # Execute function
            result = await func(*args, **kwargs)

            # Cache the result
            if result is not None:
                await cache.set(key, result, ttl or settings.CACHE_TTL)

            return result
        return wrapper
    return decorator

def invalidate_cache(*keys: str):
    """Decorator for invalidating cache keys after function execution"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)

            # Invalidate specified cache keys
            for key in keys:
                await cache.delete(key)

            return result
        return wrapper
    return decorator
