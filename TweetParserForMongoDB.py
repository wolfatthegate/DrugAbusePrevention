import copy
import json
from pprint import pprint


def _create_tweet_package(json_obj):
    tweet_map = {'tweet': _process_tweet(json_obj), 'user': _process_user(json_obj), 'place': _process_place(json_obj)}
    entities = _process_entity(json_obj)
    tweet_map['urls'] = entities['urls']
    tweet_map['media'] = entities['media']
    tweet_map['hashtags'] = entities['hashtags']
    tweet_map['symbols'] = entities['symbols']

    json_data = json.dumps(tweet_map)
    return json_data


def _process_user(json_obj):
    data = json_obj['user']
    userId = data['id']
    user = {'id': userId, 'data': data}
    return user


def _process_tweet(json_obj):
    json_copy = copy.deepcopy(json_obj)
    del json_copy['user']
    del json_copy['entities']
    del json_copy['place']
    tweetId = json_copy['id']
    tweet = {'id': tweetId, 'data': json_copy}
    return tweet


def _process_place(json_obj):
    data = json_obj['place']
    placeId = data['id']
    place = {'id': placeId, 'data': data}
    return place


def _process_entity(json_obj):
    entities = json_obj['entities']
    hashtags = entities['hashtags']
    # media = entities['media']
    urls = entities['urls']
    symbols = entities['symbols']
    # urls = [{'id': '', 'data': None}]
    # medias = [{'id': '', 'data': None}]
    # hashtags = [{'id': '', 'data': None}]
    # usermentions = []
    return {'urls': urls, 'media': [], 'hashtags': hashtags, 'symbols': symbols}


class TweetParserForMongoDB:

    def __init__(self, json_filename, verbose=0):
        self.filename = json_filename
        self.data_package = []
        self.verbose = verbose

    def extract_large_tweets(self):
        with open(self.filename, 'rb') as input_file:
            count = 0
            for line in input_file:
                obj = json.loads(line)
                tweet_package = _create_tweet_package(obj)
                if len(tweet_package) != 0:
                    self.data_package.append(tweet_package)
                if self.verbose == 1:
                    print('\n', count, ' -----------------------------------')
                    pprint(tweet_package)
                    count = count + 1


if __name__ == "__main__":
    # filename = "single_tweet.json"
    filename = "nys_tweets_filtered_2017_0.json"
    # filename = "test"
    filepath = "./data/"
    file = f"{filepath}{filename}"

    parser = TweetParserForMongoDB(file, 1)
    parser.extract_large_tweets()
