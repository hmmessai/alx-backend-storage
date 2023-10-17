#!/usr/bin/env python3
"""
Provides some stats about Nginx logs stored in MongoDB
"""
if __name__ == '__main__':
    from pymongo import MongoClient

    client = MongoClient("mongodb://127.0.0.1:27017")
    nginx_logs = client.logs.nginx

    print(nginx_logs.count_documents({}), 'logs')
    print('Methods:')
    print('\tmethod GET:', nginx_logs.count_documents({'method': 'GET'}))
    print('\tmethod GET:', nginx_logs.count_documents({'method': 'POST'}))
    print('\tmethod GET:', nginx_logs.count_documents({'method': 'PUT'}))
    print('\tmethod GET:', nginx_logs.count_documents({'method': 'PATCH'}))
    print('\tmethod GET:', nginx_logs.count_documents({'method': 'DELETE'}))
    print(nginx_logs.count_documents({'method': 'GET',
                                      'path': '/status'}), 'status check')
