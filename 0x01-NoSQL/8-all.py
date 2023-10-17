#!/usr/bin/env python3
"""
Defines list_all function
"""
import pymongo


def list_all(mongo_collection):
    """
    Lists all documents in the given collection mongo_collection
    """
    return [*mongo_colleciton.find()]
