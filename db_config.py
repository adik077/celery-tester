from pymongo import MongoClient
import os


def connection():
    connection_string = f"mongodb://{os.environ['MONGODB_USERNAME']}:{os.environ['MONGODB_PASSWORD']}@mongodb:27017/"
    client = MongoClient(connection_string)
    database = client['personal_info']
    return database['personal_info']
