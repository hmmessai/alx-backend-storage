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
    methods_list = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods_list:
        method_count = nginx_logs.count_documents({"method": method})
        print('\tmethod {}: {}'.format(method, method_count))
    status = nginx_logs.count_documents({'method': 'GET', 'path': '/status'})
    print('{} status check'.format(status))
