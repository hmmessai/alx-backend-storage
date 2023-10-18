#!/usr/bin/env python3
"""
Provides some stats about Nginx logs stored in MongoDB
"""
if __name__ == '__main__':
    from pymongo import MongoClient

    client = MongoClient()
    nginx_logs = client.logs.nginx

    num_of_docs = nginx_logs.count_documents({})
    print('{} logs'.format(num_of_docs))
    print('Methods:')
    methods_list = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods_list:
        method_count = nginx_logs.count_documents({"method": method})
        print('\tmethod {}: {}'.format(method, method_count))
    status = nginx_logs.count_documents({'method': 'GET', 'path': '/status'})
    print('{} status check'.format(status))
