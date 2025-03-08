from functools import wraps
from typing import Callable
import json

from src.core.config import get_redis

redis_client = get_redis()


def cache_response(cache_key_func: Callable, cache_timeout: int = 60):
    """
    Decorator for caching the response of a FastAPI route using Redis.
    cache_key_func: Function to generate the cache key based on the request parameters.
    cache_timeout: Time in seconds to cache the response.
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate the cache key using the provided function
            cache_key = cache_key_func(*args, **kwargs)
            
            # Try to get cached data
            cached_data = redis_client.get(cache_key)
            if cached_data:
                # If data is in the cache, return the cached response
                return json.loads(cached_data.decode('utf-8'))
            
            # If not cached, call the original function
            response = func(*args, **kwargs)
            
            # Cache the response (converted to JSON)
            redis_client.set(cache_key, json.dumps([record.dict() for record in response]), ex=cache_timeout)
            
            return response
        return wrapper
    return decorator
