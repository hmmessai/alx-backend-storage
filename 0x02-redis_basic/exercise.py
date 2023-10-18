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


def call_history(method: Callable) -> Callable:
    """store the history of inputs and outputs for a particular function"""
    input_key = method.__qualname__ + ":inputs"
    output_key = method.__qualname__ + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrap the decorated function and return the wrapper"""
        self._redis.rpush(input_key, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(result))
        return result
    return wrapper


def replay(method: Callable):
    r = redis.Redis()
    name = method.__qualname__
    count = r.get(name)
    try:
        count = int(count.decode('utf-8'))
    except Exception:
        count = 0
    print("{} was called {} times".format(name, count))
    inputs = r.lrange(name+":inputs", 0, -1)
    outputs = r.lrange(name+":outputs", 0, -1)
    for inp, outp in zip(inputs, outputs):
        try:
            inp = inp.decode('utf-8')
        except Exception:
            inp = ""
        try:
            outp = outp.decode('utf-8')
        except Exception:
            outp = ""
        print("{}(*{}) -> {}".format(name, inp, outp))


class Cache:
    """
    Representation of Cache class
    """
    def __init__(self):
        """Initializes the Cache instance"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
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
