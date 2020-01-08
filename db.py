import pymongo
from datetime import datetime
from settings import username, password, database, hostname

client = pymongo.MongoClient(f'mongodb://{username}:{password}@{hostname}:27017/{database}')
raspberrydb = client[database]
collection = raspberrydb["pidata"]

raspberrydb["pilogin"].insert_one({"login_time": datetime.now()})
