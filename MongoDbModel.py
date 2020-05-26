from pymongo import MongoClient


class TweetStore:
    collections = ['tweet', 'user', 'place', 'hashtag', 'symbol', 'url']


class MongoDbModel:

    def __init__(self, uri, username, password, verbose=0):
        client = MongoClient('localhost', 27017)
        self.db = client['twitter']
        self.username = username
        self.password = password
        self.verbose = verbose

    def insertOne(self, id, data, tableName):
        if tableName in self.db.list_collection_names():
            collection = self.db[tableName]
            id = collection.insert_one(data).inserted_id
            if self.verbose == 1:
                print(id)

    def insertBulk(self, data, tableName):
        if tableName in self.db.list_collection_names():
            collection = self.db[tableName]
            collection.bulk_write(data)

    def close(self):
        self.db.quit()
