#!/usr/bin/env python3
"""
Define insert school function
"""


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document in a collection bases on kwargs
    """
    new = mongo_collection.insert_one(kwargs)
    return new.inserted_id
