from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.cv06
collection = db.restaurants