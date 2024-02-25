from datetime import datetime
from time import sleep
import json
import redis
from pymongo import MongoClient
from utils import index_validation
from config import REDIS_HOST, REDIS_PORT , REDIS_LAST , MONGO_CS , MONGO_COLLECTION , MONGO_DB , SLEEP , ENCODING , DATETIME_FORMAT

REDIS_CLIENT = redis.Redis(REDIS_HOST , REDIS_PORT)
MONGO_CLIENT = MongoClient(MONGO_CS)
EVENTS = MONGO_CLIENT[MONGO_DB][MONGO_COLLECTION]

def main():
    index_validation(collection=EVENTS, index_name="timestamp")
    latest_stamp = REDIS_CLIENT.get(REDIS_LAST)
    query = {}

    if latest_stamp is not None:
        latest_stamp = latest_stamp.decode(ENCODING)
        latest_stamp = datetime.strptime(latest_stamp, DATETIME_FORMAT)
        query = {"timestamp": {"$gt": latest_stamp}}

    while True:        
        mapping = {}

        for event in EVENTS.find(query):
            # update latest_stamp
            if latest_stamp is None or event["timestamp"] > latest_stamp:
                latest_stamp = event["timestamp"]
                mapping[REDIS_LAST] = datetime.strftime(event["timestamp"], DATETIME_FORMAT)
                query = {"timestamp": {"$gt": latest_stamp}}

            # format object for later json parsing
            del event['_id'] # remove mongo's _id from event
            event["timestamp"] = datetime.strftime(event["timestamp"], DATETIME_FORMAT)

            # create key and json value for mapping
            key = f'{event["reporterId"]}:{event["timestamp"]}'
            value = json.dumps(event).encode(ENCODING)
            mapping[key] = value

        if len(mapping) > 0:
            REDIS_CLIENT.mset(mapping)  
            
        print(f'inserting {len(mapping)} keys')
            
        sleep(SLEEP) 

if __name__ == '__main__':
    main()