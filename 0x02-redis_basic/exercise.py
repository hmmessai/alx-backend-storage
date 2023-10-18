#!/usr/bin/env python3
"""
Defines the Cache class
"""
import redis
import uuid
from typing import Union
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """counts how many times methods of Cache class are called"""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrap the decorated function and return the wrapper"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """
    Representation of Cache class
    """
    def __init__(self):
        """Initializes the Cache instance"""
        self._redis = redis.Redis()
        self._redis.flushdb()
    
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Stores new data with randomly generated key"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """Converts data back to the desired format"""
        data = self._redis.get(key)
        if fn:
            data = fn(data)
        return data

    def get_str(self, key: str) -> str:
        '''parametrize Cache.get with correct conversion function'''
        value = self._redis.get(key)
        return value.decode('utf-8')

    def get_int(self, key: str) -> int:
        '''parametrize Cache.get with correct conversion function'''
        value = self._redis.get(key)
        try:
            value = int(value.decode('utf-8'))
        except Exception:
            value = 0
        return value
