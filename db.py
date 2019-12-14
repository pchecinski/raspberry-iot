import pymongo
from datetime import datetime
from creditientials import username, password, database

client = pymongo.MongoClient(f'mongodb://{username}:{password}@mongo.checinski.dev:27017/{database}')
raspberrydb = client[database]
collection = raspberrydb["pidata"]

raspberrydb["pilogin"].insert_one({"login_time": datetime.now()})
