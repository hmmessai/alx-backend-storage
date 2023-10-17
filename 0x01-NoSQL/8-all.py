#!/usr/bin/env python3
"""
Defines list_all function
"""


def list_all(mongo_collection):
    """
    Lists all documents in the given collection mongo_collection
    """
    return [doc for doc in mongo_colleciton.find()]
