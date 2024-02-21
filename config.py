import yaml

with open("config.yaml" , 'r') as f:
    config = yaml.safe_load(f)

REDIS_HOST = config["REDIS_HOST"]
REDIS_PORT = config["REDIS_PORT"]
REDIS_LAST = config["REDIS_LAST"]

MONGO_CS = config["MONGO_CS"]
MONGO_DB = config["MONGO_DB"]
MONGO_COLLECTION = config["MONGO_COLLECTION"]

SLEEP = config["SLEEP"]
ENCODING = config["ENCODING"]
DATETIME_FORMAT = config["DATETIME_FORMAT"]