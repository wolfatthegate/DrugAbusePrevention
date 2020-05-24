from pprint import pprint

from neo4j import GraphDatabase


class GraphDbModel:

    def __init__(self, uri, user, password, verbose=0):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.verbose = verbose

    def close(self):
        self.driver.close()

    def insert(self, tweets):
        with self.driver.session() as session:
            count = 1
            for tweet in tweets:
                if count == 1:
                    print(tweet)
                if count == 22:
                    print(tweet)

                message = session.write_transaction(self._create_and_return_tweet, tweet)
                if self.verbose == 1:
                    print(count, '.\t', message)
                count = count + 1

    @staticmethod
    def _create_and_return_tweet(tx, tweet):
        result = tx.run("MERGE (t:tweet) on create SET t.id = $tweet.id "
                        "MERGE (u:user) on create SET u.id=$tweet.userId "
                        "MERGE (l:location) on create SET l.id=$tweet.locationId "
                        "MERGE (p:place) on create SET p.id=$tweet.placeId "
                        "MERGE (u)-[:at]->(l) "
                        "MERGE (u)-[:send]->(t) "
                        "MERGE (t)-[:tag]->(p) "
                        # "FOREACH (val IN $tweet.hashtags | MERGE (h:hashtag) on create SET h.id=val MERGE (t)-[:tag]->(h))"
                        # "FOREACH (val IN $tweet.urls | MERGE (url:url) on create SET url.id=val MERGE (t)-[:include]->(url))"
                        # "FOREACH (val IN $tweet.medias | MERGE (m:media) on create SET  m.id=val MERGE (t)-[:has]->(m))"
                        # "FOREACH (val IN $tweet.user_mentions | MERGE (u1:user)  on create SET u1.id=val MERGE (t)-[:mention]->(u1)) "
                        "RETURN 'User: '+ u.id + ' sent '+ 'tweet: '+ t.id ", tweet=tweet)
        return result.single()[0]


if __name__ == "__main__":
    graphModel = GraphDbModel("bolt://localhost:7687", "neo4j", "test", 1)
    tweet1 = {'id': 3, 'userId': '1', 'locationId': 'l1', 'placeId': 'p1', 'hashtags': [], 'urls': [], 'medias': [],
              'user_mentions': []}
    tweet2 = {'id': 4, 'userId': '2', 'locationId': 'l2', 'placeId': 'p2', 'hashtags': [], 'urls': [], 'medias': [],
              'user_mentions': []}
    tweets = [tweet1, tweet2]
    graphModel.insert(tweets)
    graphModel.close()
