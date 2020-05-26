import json

from TweetParser import TweetParser
from dbModels.GraphDbModel import GraphDbModel
from dbModels.MongoDbModel import MongoDbModel


def main():
    # filename = "single_tweet.json"
    filename = "nys_tweets_filtered_2017_0.json"
    # filename = "test"
    filepath = "./data/"
    file = f"{filepath}{filename}"

    parser = TweetParser(file)
    parser.extract_large_tweets(1)

    graphModel = GraphDbModel("bolt://localhost:7687", "neo4j", "test", 1)
    graphModel.insert(parser.tweets)
    graphModel.close()

    mongoDbModel = MongoDbModel('mongodb://localhost:27017/', 'twitter')
    mongo_data = parser.data_package
    for each_data in mongo_data:
        print(each_data)
        json_data = json.loads(each_data)
        for tableName in json_data.keys():
            value = json_data[tableName]
            if len(value) != 0:
                print(tableName, '\t', value)
                res = mongoDbModel.insert(value['id'], value['data'], tableName)
                print(res)


if __name__ == '__main__':
    main()
