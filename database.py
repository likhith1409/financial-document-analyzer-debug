import pymongo
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self, uri):
        self.client = pymongo.MongoClient(uri)
        self.db = self.client.get_default_database()
        self.collection = self.db["analysis_results"]

    def insert_result(self, data):
        return self.collection.insert_one(data).inserted_id

    def get_result(self, result_id):
        return self.collection.find_one({"_id": ObjectId(result_id)})

    def get_results_by_username(self, username):
        # Fetches all analysis results for a specific user, sorted by creation date
        return list(self.collection.find({"username": username}).sort("created_at", -1))

# The MongoDB connection string is loaded from the environment variables.
db = Database(os.getenv("MONGO_URI"))
