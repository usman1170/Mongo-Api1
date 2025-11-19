from pymongo import MongoClient
import os

class MongoDBManager:
    def __init__(self, database="test_api"):
        self.client = MongoClient(os.getenv("MONGO_URI"))
        self.db = self.client[database]
        
        # collections 
        self.users = self.db["users"]
        self.posts = self.db["posts"]
        
        