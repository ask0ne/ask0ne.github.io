import os
import json
import pickle
from datetime import datetime, timedelta
from typing import Optional, Any, Dict
from functools import wraps
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_app() -> FastAPI:
    app = FastAPI(title="atharva")
    
    # Mount static files
    app.mount("/static", StaticFiles(directory="static"), name="static")
    
    return app

# Caching configuration
CACHE_EXPIRE_TIME = int(os.getenv("CACHE_EXPIRE_TIME", "86400"))  # 24 hours default
USE_REDIS = os.getenv("USE_REDIS", "false").lower() == "true"
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# In-memory cache as fallback
_memory_cache: Dict[str, Dict[str, Any]] = {}

class CacheManager:
    """Simple cache manager with Redis fallback to in-memory"""
    
    def __init__(self):
        self.redis_client = None
        if USE_REDIS:
            try:
                import redis
                self.redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)
                self.redis_client.ping()  # Test connection
            except Exception as e:
                print(f"Redis connection failed: {e}. Using in-memory cache.")
                self.redis_client = None
    
    def get(self, key: str) -> Optional[Any]:
        """Get cached value"""
        if self.redis_client:
            try:
                cached_data = self.redis_client.get(key)
                if cached_data:
                    return pickle.loads(cached_data.encode('latin1'))
            except Exception as e:
                print(f"Redis get error: {e}")
        
        # Fallback to memory cache
        if key in _memory_cache:
            cache_entry = _memory_cache[key]
            if datetime.now() < cache_entry['expires']:
                return cache_entry['data']
            else:
                del _memory_cache[key]
        
        return None
    
    def set(self, key: str, value: Any, expire_seconds: int = CACHE_EXPIRE_TIME) -> bool:
        """Set cached value"""
        if self.redis_client:
            try:
                serialized = pickle.dumps(value).decode('latin1')
                return self.redis_client.setex(key, expire_seconds, serialized)
            except Exception as e:
                print(f"Redis set error: {e}")
        
        # Fallback to memory cache
        _memory_cache[key] = {
            'data': value,
            'expires': datetime.now() + timedelta(seconds=expire_seconds)
        }
        return True
    
    def delete(self, key: str) -> bool:
        """Delete cached value"""
        if self.redis_client:
            try:
                self.redis_client.delete(key)
            except Exception:
                pass
        
        if key in _memory_cache:
            del _memory_cache[key]
        return True
    
    def clear_prefix(self, prefix: str) -> bool:
        """Clear all keys with given prefix"""
        if self.redis_client:
            try:
                keys = self.redis_client.keys(f"{prefix}*")
                if keys:
                    self.redis_client.delete(*keys)
            except Exception:
                pass
        
        # Clear memory cache
        keys_to_delete = [key for key in _memory_cache.keys() if key.startswith(prefix)]
        for key in keys_to_delete:
            del _memory_cache[key]
        return True
    
    def get_cache_info(self) -> dict:
        """Get cache information"""
        return {
            "cache_enabled": True,
            "cache_expire_time": CACHE_EXPIRE_TIME,
            "redis_enabled": self.redis_client is not None,
            "cache_type": "Redis" if self.redis_client else "In-Memory",
            "memory_cache_entries": len(_memory_cache)
        }

# Global cache instance
cache_manager = CacheManager()

# Templates configuration
templates = Jinja2Templates(directory="templates")

def cache_key(*args, **kwargs) -> str:
    """Generate cache key from arguments"""
    key_parts = [str(arg) for arg in args]
    key_parts.extend([f"{k}:{v}" for k, v in sorted(kwargs.items())])
    return "blog:" + ":".join(key_parts)

def cached(expire_seconds: int = CACHE_EXPIRE_TIME, key_prefix: str = ""):
    """Caching decorator for functions"""
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Generate cache key
            cache_key_str = f"{key_prefix}:{func.__name__}:{hash(str(args) + str(sorted(kwargs.items())))}"
            
            # Try to get from cache
            cached_result = cache_manager.get(cache_key_str)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            cache_manager.set(cache_key_str, result, expire_seconds)
            return result
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            # Generate cache key
            cache_key_str = f"{key_prefix}:{func.__name__}:{hash(str(args) + str(sorted(kwargs.items())))}"
            
            # Try to get from cache
            cached_result = cache_manager.get(cache_key_str)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            cache_manager.set(cache_key_str, result, expire_seconds)
            return result
        
        # Return appropriate wrapper based on function type
        if hasattr(func, '__code__') and func.__code__.co_flags & 0x80:  # CO_COROUTINE
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator