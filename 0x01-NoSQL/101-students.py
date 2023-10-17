#!/usr/bin/env python3
"""
Define top_students function
"""


def top_students(mongo_collection):
    """
    Returns all students sorted by average score
    """
    return mongo_collection.aggregate([
                                {Sproject: {
                                    name: 1,
                                    averagescore:
                                        {$avg: "$topics.score"}
                                    },
                                    topics: 1},
                                {$sort: {average: -1}}
                            ])
