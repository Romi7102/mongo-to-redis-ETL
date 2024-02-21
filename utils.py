from pymongo import ASCENDING

def index_validation(collection, index_name):
    """ensure that index exists and if it doesn't exist create it"""
    existing_indexes = collection.list_indexes()
    index_exists = any(index["name"] == index_name for index in existing_indexes)
    if index_exists is False:
        collection.create_index([("timestamp", ASCENDING)])