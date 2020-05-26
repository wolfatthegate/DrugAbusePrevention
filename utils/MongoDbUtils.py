import copy
import json


def make_data(json_obj):
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

