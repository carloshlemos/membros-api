import os

from pymongo import MongoClient


def get_mongodb():
    host = os.getenv("MONGO_HOST")
    username = os.getenv("MONGO_USERNAME")
    password = os.getenv("MONGO_PASSWORD")
    db_name = os.getenv("MONGO_DB_NAME")
    mode = os.getenv('MODE', 'development')
    tls = '&tls=true' if mode == 'production' else ''
    uri = f"mongodb://{username}:{password}@{host}/{db_name}?authSource=admin&retryWrites=true&w=majority{tls}"

    client = MongoClient(uri)
    return client[db_name]
