#!/usr/bin/env python3
"""
Define get page function
"""
import requests
import redis
from functools import wraps
from typing import Callable


def count(func: Callable):
    """Counts how many times a function has been called and cache it"""
    @wraps(func)
    def wrapper(url):
        """Wrapper function"""
        r = redis.Redis()
        cached_key = "cached:{}".format(url)
        cached_data = r.get(cached_key)
        if cached_data:
            return cached_data.decode('utf-8')

        count_key = "count:" + url
        html = func(url)

        r.incr(count_key)
        r.set(cached_key, html)
        r.expire(cached_key, 10)
        return html
    return wrapper


@count
def get_page(url: str) -> str:
    """
    Obtains html content of url and returns it
    """
    response = requests.get(url)
    page = response.text
    return page
