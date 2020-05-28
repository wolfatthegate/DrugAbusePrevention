from pymongo import MongoClient


class TweetStore:
    collections = ['tweet', 'user', 'place', 'hashtags', 'symbol', 'url']
    index_map = {'tweet': ['id'],
                 'user': ['id', 'screen_name'],
                 'place': ['id', 'name'],
                 # 'hashtags': []
                 }


class MongoDbModel:

    def __init__(self, uri, database, verbose=0):
        try:
            self.client = MongoClient('localhost', 27017)
            self.db = self.client[database]
            self.verbose = verbose
        except Exception as e:
            print(str(e))

    def create_index(self):
        for table in TweetStore.collections:
            self.db[table].createIndex({"_id": 1})

    # Insert json array [{data1}, {data2}]
    def insert(self, id, data, tableName):
        try:
            collection = self.db[tableName]
            # if len(data) != 0:
            ids = collection.insert(data).inserted_ids
            if self.verbose == 1:
                print('Inserted {} in table {} \t res: {}'.format(data, tableName, ids))
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
        self.client.close()
