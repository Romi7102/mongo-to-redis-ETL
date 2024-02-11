from datetime import datetime
from time import sleep
import os
import json
import redis
from pymongo import MongoClient

REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')
REDIS_CLIENT = redis.Redis(REDIS_HOST , REDIS_PORT)

MONGO_CS = os.environ.get('MONGO_CS')
MONGO_CLIENT = MongoClient(MONGO_CS)

def latest_timestamp():
    ret = None

    for key in REDIS_CLIENT.keys('*'):
        json_str = REDIS_CLIENT.get(key)
        json_obj = json.loads(json_str)

        timestamp_string = json_obj['timestamp']

        if timestamp_string:
            timestamp = datetime.strptime(timestamp_string, "%Y-%m-%d %H:%M:%S")

            if ret is None or timestamp > ret:
                ret = timestamp
    return ret


def main():

    events = MONGO_CLIENT.testdb.events
    latest_stamp = latest_timestamp()
    query = {}

    while True:
        if latest_stamp:
            query = {"timestamp": {"$gt": latest_stamp}}
            print(latest_stamp)
        for event in events.find(query):
            # remove mongo _id
            del event["_id"]

            # change the latest timestamp 
            latest_stamp = event["timestamp"]

            # format timestamp to string
            event["timestamp"] = datetime.strftime(event["timestamp"] ,"%Y-%m-%d %H:%M:%S")

            #insert to redis
            key = f'{event["reporterId"]}:{event["timestamp"]}'
            value = json.dumps(event).encode('utf8')
            REDIS_CLIENT.set(key, value)

        sleep(5) #needs to be 30 , for convenience set to 5

if __name__ == '__main__':
    main()