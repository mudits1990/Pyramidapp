__author__ = 'mudit'
from pymongo import MongoClient
import datetime
import json

class adapter():
    def createColletion(self, collection_name):
        client = MongoClient()
        db = client.sfdc_database
        collection = db[collection_name]
        return collection
    def insert_posts(self, collection_name, post):
        return collection_name.insert(post)

