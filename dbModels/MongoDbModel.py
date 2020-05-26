from pymongo import MongoClient


class TweetStore:
    collections = ['tweet', 'user', 'place', 'hashtag', 'symbol', 'url']


class MongoDbModel:

    def __init__(self, uri, database, verbose=0):
        client = MongoClient('localhost', 27017)
        self.db = client[database]
        self.verbose = verbose

    # Insert json array [{data1}, {data2}]
    def insert(self, id, data, tableName):
        try:
            collection = self.db[tableName]
            ids = collection.insert(data).inserted_ids
            if self.verbose == 1:
                print(ids)
            return ids

        except Exception as e:
            print(str(e))

    def update(self, id, data, tableName):
        try:
            collection = self.db[tableName]
            collection.update_one({'id': id}, data, upsert=True)
        except Exception as e:
            print(str(e))

    def select(self, tableName):
        try:
            col = self.db[tableName].find()
            print('\n All data from EmployeeData Database \n')
            for emp in col:
                print(emp)

        except Exception as e:
            print(str(e))

    def close(self):
        self.db.quit()
