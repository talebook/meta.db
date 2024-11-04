#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib
import random
import string
import pymongo


# 假设已经连接到MongoDB数据库
mongo_client = None
mongo_db = None 

def init(mongo_addr):
    global mongo_client, mongo_db
    mongo_client = pymongo.MongoClient(mongo_addr)
    mongo_db = mongo_client["mydatabase"]

# User类
class User:
    def __init__(self, email, password, salt, api_key):
        self._table = mongo_db["users"]
        self.email = email
        self.password = password
        self.salt = salt
        self.api_key = api_key

    def save(self):
        self._table.insert_one(self.__dict__)

    def reset_password(self):
        new_password = self.random_string(16)
        self.salt = self.random_string(16)
        new_hashed_password = self.hash_password(new_password, self.salt)

        self.password = new_hashed_password
        self.save()

        return new_password

    def random_string(self, len=16):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=len))

    def hash_password(self, password, salt):
        return hashlib.sha256((password + salt).encode()).hexdigest()

    def generate_api_key(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=32))


class Book:
    def __init__(self):
        self._table = mongo_db["books"]

    def save(self, book):
        self._table.insert_one(book)

    def search(self, title):
        return self._table.find({"title": {"$regex": title}}).limit(10)