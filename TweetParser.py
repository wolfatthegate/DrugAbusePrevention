import json

# Parse json file
from utils import MongoDbUtils, GraphDbUtils


class TweetParser:

    def __init__(self, json_filename):
        self.filename = json_filename
        self.tweets = []
        self.data_package = []

    def extract_large_tweets(self, verbose=0):
        with open(self.filename, 'rb') as input_file:
            count = 0
            for line in input_file:
                obj = json.loads(line)
                tweet = GraphDbUtils.make_data(obj)
                tweet_package = MongoDbUtils.make_data(obj)

                if len(tweet) != 0:
                    self.tweets.append(tweet)
                if len(tweet_package) != 0:
                    self.data_package.append(tweet_package)
                if verbose == 1:
                    # print(count, '. \t ', tweet)
                    print(count, '. \t ', tweet_package)
                    count = count + 1


if __name__ == "__main__":
    # filename = "single_tweet.json"
    filename = "nys_tweets_filtered_2017_0.json"
    # filename = "test"
    filepath = "./data/"
    file = f"{filepath}{filename}"

    parser = TweetParser(file)
    parser.extract_large_tweets(1)
