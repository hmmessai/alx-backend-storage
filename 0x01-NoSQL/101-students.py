#!/usr/bin/env python3
"""
Define top_students function
"""


def top_students(mongo_collection):
    """
    Returns all students sorted by average score
    """
    pipeline = [
            {
                '$project': {
                    'name': 1,
                    'averagescore': {
                        '$avg': '$topics.score'
                    },
                    'topics': 1
                }
            },
            {
                '$sort': {
                    'averagescore': -1
                }
            },
        ]
    return mongo_collection.aggregate(pipeline)
