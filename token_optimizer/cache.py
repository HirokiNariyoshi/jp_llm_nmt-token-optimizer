"""
Caching layer for translations and LLM responses.
"""

import json
from typing import Optional, Any
import hashlib


class CacheManager:
    """Manages caching operations."""
    
    def __init__(self, enabled: bool = True, redis_config: Optional[dict] = None):
        """
        Initialize cache manager.
        
        Args:
            enabled: Whether caching is enabled
            redis_config: Redis configuration dict (host, port, db, password, ttl)
        """
        self.enabled = enabled
        self.redis_client = None
        self.ttl = 86400  # Default 24 hours
        
        if enabled and redis_config:
            try:
                import redis
                self.redis_client = redis.Redis(
                    host=redis_config.get("host", "localhost"),
                    port=redis_config.get("port", 6379),
                    db=redis_config.get("db", 0),
                    password=redis_config.get("password"),
                    decode_responses=True
                )
                self.ttl = redis_config.get("ttl", 86400)
                # Test connection
                self.redis_client.ping()
            except ImportError:
                print("Warning: redis-py not installed. Caching disabled.")
                self.enabled = False
            except Exception as e:
                print(f"Warning: Redis connection failed: {e}. Caching disabled.")
                self.enabled = False
    
    def get(self, key: str) -> Optional[str]:
        """
        Get value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found
        """
        if not self.enabled or not self.redis_client:
            return None
        
        try:
            return self.redis_client.get(key)
        except Exception as e:
            print(f"Cache get error: {e}")
            return None
    
    def set(self, key: str, value: str, ttl: Optional[int] = None) -> bool:
        """
        Set value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds (uses default if not specified)
            
        Returns:
            True if successful, False otherwise
        """
        if not self.enabled or not self.redis_client:
            return False
        
        try:
            ttl = ttl or self.ttl
            self.redis_client.setex(key, ttl, value)
            return True
        except Exception as e:
            print(f"Cache set error: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """Delete key from cache."""
        if not self.enabled or not self.redis_client:
            return False
        
        try:
            self.redis_client.delete(key)
            return True
        except Exception as e:
            print(f"Cache delete error: {e}")
            return False
    
    def clear(self) -> bool:
        """Clear all cache entries."""
        if not self.enabled or not self.redis_client:
            return False
        
        try:
            self.redis_client.flushdb()
            return True
        except Exception as e:
            print(f"Cache clear error: {e}")
            return False
    
    @staticmethod
    def generate_key(prefix: str, *args) -> str:
        """
        Generate a cache key from prefix and arguments.
        
        Args:
            prefix: Key prefix
            *args: Arguments to include in key
            
        Returns:
            Generated cache key
        """
        content = ":".join(str(arg) for arg in args)
        hash_value = hashlib.md5(content.encode()).hexdigest()
        return f"{prefix}:{hash_value}"
