#!/usr/bin/env python3
"""
provides some stats about Nginx logs stored in MongoDB
with the top 10 of the most present IPs in the collection
"""

if __name__ == '__main__':
    from pymongo import MongoClient

    client = MongoClient("mongodb://127.0.0.1:27017")
    nginx_logs = client.logs.nginx

    print(nginx_logs.count_documents({}), 'logs')
    print('Methods:')
    print('    method GET:', nginx_logs.count_documents({'method': 'GET'}))
    print('    method POST:', nginx_logs.count_documents({'method': 'POST'}))
    print('    method PUT:', nginx_logs.count_documents({'method': 'PUT'}))
    print('    method PATCH:', nginx_logs.count_documents({'method': 'PATCH'}))
    print('    method DELETE:', nginx_logs.count_documents({'method': 'DELETE'}))
    print(nginx_logs.count_documents({'method': 'GET',
                                      'path': '/status'}), 'status check')

    print("IPs:")
    ip_list = nginx_logs.aggregate([
        {'$group': {
            '_id': '$ip',
            'count': {'$sum': 1}
        }},
        {'$sort': {'count': -1}},
        {'$limit': 10},
        {'$project': {
            '_id': 0,
            'ip': '$_id',
            'count': 1
        }}
    ])

    for ip in ip_list:
        print('\t{}: {}'.format(ip.get('ip'), ip.get('count')))
