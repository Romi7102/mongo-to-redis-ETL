from datetime import datetime
from time import sleep
import os
import json
import redis
from pymongo import MongoClient
from pymongo import ASCENDING

REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')
REDIS_CLIENT = redis.Redis(REDIS_HOST , REDIS_PORT)
REDIS_LAST = os.environ.get("REDIS_LAST")

MONGO_CS = os.environ.get('MONGO_CS')
MONGO_DB = os.environ.get('MONGO_DB')
MONGO_COLLECTION = os.environ.get('MONGO_COLLECTION')
MONGO_CLIENT = MongoClient(MONGO_CS)

SLEEP = int(os.environ.get('SLEEP'))

def main():

    events = MONGO_CLIENT[MONGO_DB][MONGO_COLLECTION]
    latest_stamp = REDIS_CLIENT.get(REDIS_LAST)
    print(latest_stamp)
    query = {}
    if latest_stamp is not None:
        latest_stamp = latest_stamp.decode('utf8')
        latest_stamp = datetime.strptime(latest_stamp, "%Y-%m-%d %H:%M:%S")
        query = {"timestamp": {"$gt": latest_stamp}}

    # ensure that index exists and if it doesn't exist create it
    existing_indexes = events.list_indexes()
    index_name_to_check = "timestamp"
    index_exists = any(index["name"] == index_name_to_check for index in existing_indexes)
    if index_exists is False:
        events.create_index([("timestamp", ASCENDING)])

    while True:
        
        for event in events.find(query): #todo: redis mset ( multiple keys set)
            # remove mongo _id
            del event["_id"]

            # change the latest timestamp
            if latest_stamp is None or event["timestamp"] > latest_stamp:
                latest_stamp = event["timestamp"]
                REDIS_CLIENT.set(REDIS_LAST, datetime.strftime(event["timestamp"], "%Y-%m-%d %H:%M:%S"))
                query = {"timestamp": {"$gt": latest_stamp}}

            # format timestamp to string
            event["timestamp"] = datetime.strftime(event["timestamp"] ,"%Y-%m-%d %H:%M:%S")

            #insert to redis
            key = f'{event["reporterId"]}:{event["timestamp"]}'
            value = json.dumps(event).encode('utf8')
            REDIS_CLIENT.set(key, value)


        sleep(SLEEP) #needs to be 30 , for convenience set to 5 

if __name__ == '__main__':
    main()