# mongo-to-redis-ETL
This Python ETL (Extract, Transform, Load) script pulls data from MongoDB, performs transformations, and inserts it into a Redis database. The script is designed to handle JSON objects representing events with timestamps and reporter IDs, ensuring that duplicate events are not inserted into the Redis database.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)

## Installation

1. Clone this repository:

    ```git clone https://github.com/Romi7102/mongo-to-redis-ETL.git```

2. Install the required dependencies:
    
    ``` pip install -r requirements.txt```


## Usage

1. Ensure that you have a running Redis server and a MongoDB instance.

2. Build the docker image using the dokcer file

    ```dokcer build -t mongo-to-redis-etl .```

3. Run the image with the following environment variables

    ```docker run -e REDIS_HOST=<redis host> -e REDIS_PORT=<redis port> -e REDIS_LAST=<redis key> -e MONGO_CS=<mongo connection string> -e MONGO_DB=<database name> -e MONGO_COLLECTION=<collection name> -e SLEEP=<time between insertions> mongo-to-redis-etl```

    ### Environment Variables
    
    REDIS_PORT: This environment variable specifies the port number on which the Redis server is listening. Redis typically defaults to port 6379, but if your Redis server is configured to listen on a different port, you can set this variable to that port number. For example, if your Redis server is configured to listen on port 6380, you would set REDIS_PORT to 6380.

    REDIS_HOST: This environment variable specifies the host address (or IP address) of the Redis server. If Redis is running on the same machine where your Python script is executed, you can typically set this variable to localhost or 127.0.0.1. If Redis is running on a different machine within your network, you would set this variable to the IP address or hostname of that machine.

    REDIS_LAST: This environment variable specifies the redis key that will be used to save the last insertion time of an event to redis.

    MONGO_CS: This environment variable specifies the connection URI for your MongoDB database. It should include the protocol (e.g., mongodb://), hostname, port number, and any authentication credentials if required.

    MONGO_DB: This environment variable specifies the database to connect to. 

    MONGO_COLLECTION: This environment variable specifies the collection to pull data from.

    SLEEP: This environment variable specifies the number of seconds to sleep between each insertion.





## Running without docker

Alternatively, you can run the project locally , you would just need a way to load environment variables so the main.py file will recognize them , you can use any way you see fit.