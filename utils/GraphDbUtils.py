import json


def make_data(json_obj: json) -> json:
    userId = json_obj['user']['id']
    tweetId = json_obj['id']
    locationId = json_obj['user']['location']
    placeId = json_obj['place']['id']

    # todo need to parse hashtags, urls, medias, user_mentions
    # todo need to handle null location
    if not locationId:
        locationId = 'l'

    tweet = {'id': tweetId, 'userId': userId, 'locationId': locationId, 'placeId': placeId, 'hashtags': [], 'urls': [],
             'medias': [], 'user_mentions': []}

    if userId and tweetId and locationId and placeId:
        return tweet
    else:
        print('---- Empty ---- \t', tweet)
        return {}
