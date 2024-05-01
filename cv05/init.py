from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.cv05
collection = db.restaurants
