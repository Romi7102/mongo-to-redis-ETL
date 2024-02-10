from datetime import datetime
from time import sleep
import json
import redis
from pymongo import MongoClient

def latest_timestamp():
    r = redis.Redis(host='localhost' , port=6379)
    latest_timestamp = None

    for key in r.keys('*'):
        json_str = r.get(key)
        json_obj = json.loads(json_str)

        timestamp_string = json_obj['timestamp']

        if timestamp_string:
            timestamp = datetime.strptime(timestamp_string, "%Y-%m-%d %H:%M:%S")

            if latest_timestamp is None or timestamp > latest_timestamp:
                latest_timestamp = timestamp
    
    return latest_timestamp


def main():
    #! get from enviroment variables
    r = redis.Redis(host='localhost' , port=6379)
    mongo_client = MongoClient('mongodb://admin:admin@localhost:27017')
    events = mongo_client.testdb.events
    latest_stamp = latest_timestamp()
    query = {}

    while True:

        if latest_stamp:
            query = {"timestamp": {"$gt": latest_stamp}}
            print(latest_stamp)
        
        for event in events.find(query):
            
            # i dont need the mongo id in the redis database , might as well remove it now
            del event["_id"] 

            # change the latest timestamp 
            latest_stamp = event["timestamp"]

            # format timestamp to string
            event["timestamp"] = datetime.strftime(event["timestamp"] ,"%Y-%m-%d %H:%M:%S")

            #insert to redis
            key = f'{event["reporterId"]}:{event["timestamp"]}'
            value = json.dumps(event).encode('utf8')
            r.set(key, value)

        sleep(5)

if __name__ == '__main__':
    main()