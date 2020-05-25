import json

import ijson


# Parse json file
from GraphDbModel import GraphDbModel


def _create_tweet_model(json_obj):
    userId = json_obj['user']['id']
    tweetId = json_obj['id']
    locationId = json_obj['user']['location']
    placeId = json_obj['place']['id']

    # todo need to parse hashtags, urls, medias, user_mentions
    # todo need to handle null location
    if not locationId:
        locationId = 'l'

    tweet = {'id': tweetId, 'userId': userId, 'locationId': locationId, 'placeId': placeId, 'hashtags': [], 'urls': [], 'medias': [], 'user_mentions': []}

    if userId and tweetId and locationId and placeId:
        return tweet
    else:
        print('---- Empty ---- \t', tweet)
        return {}


class TweetParser:

    def __init__(self, json_filename):
        self.filename = json_filename
        self.tweets = []

    def viewContent(self, json_filename):
        """   Print json content   """
        with open(json_filename) as jsonfile:
            content = jsonfile.read()
            print(f"\n{content}\n")

    def extract_large_tweets(self, verbose=0):
        with open(self.filename, 'rb') as input_file:
            count = 0
            for line in input_file:
                obj = json.loads(line)
                tweet = _create_tweet_model(obj)
                if len(tweet) != 0:
                    self.tweets.append(tweet)
                if verbose == 1:
                    print(count, '. \t', tweet)
                    count = count + 1

    def extract_tweets(self):
        with open(self.filename, 'rb') as input_file:
            # for line in input_file:
            userId = ijson.items(input_file, 'user.id')
            tweetId = ijson.items(input_file, 'id')
            locationId = ijson.items(input_file, 'user.location')
            placeId = ijson.items(input_file, 'place.id')
            input_file.close()
            tweet = {}
            print('\n tweetId: {} \n'.format(tweetId))

            tweet.setdefault('id', tweetId)
            tweet.setdefault('userId', userId)
            tweet.setdefault('locationId', locationId)
            tweet.setdefault('placeId', placeId)
            tweet.setdefault('hashtags', [])
            tweet.setdefault('urls', [])
            tweet.setdefault('medias', [])
            tweet.setdefault('user_mentions', [])
            # tweet = {'id': tweetId, 'userId': userId, 'locationId': locationId, 'placeId': placeId, 'hashtags': [], 'urls': [], 'medias': [], 'user_mentions': []}
            print(tweet)
            self.tweets.append(tweet)


if __name__ == "__main__":
    # filename = "single_tweet.json"
    filename = "nys_tweets_filtered_2017_0.json"
    # filename = "test"
    filepath = "./data/"
    file = f"{filepath}{filename}"

    parser = TweetParser(file)
    parser.extract_large_tweets()
    graphModel = GraphDbModel("bolt://localhost:7687", "neo4j", "test", 1)
    graphModel.insert(parser.tweets)
    graphModel.close()

