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
            message = session.write_transaction(self._create_and_return_tweet, tweets)
            if self.verbose == 1:
                print(message)
                # print(tweets)

    @staticmethod
    def _create_and_return_tweet(tx, tweets):
        result = tx.run("UNWIND $tweets as tweet "
                        "MERGE (t:tweet {id:tweet.id}) "
                        "MERGE (u:user {id:tweet.userId}) "
                        "MERGE (l:location {id:tweet.locationId}) "
                        "MERGE (p:place {id:tweet.placeId}) "
                        "MERGE (u)-[:at]->(l) "
                        "MERGE (u)-[:send]->(t) "
                        "MERGE (t)-[:tag]->(p) "
                        "FOREACH (val IN tweet.hashtags | MERGE (h:hashtag) on create SET h.id=val MERGE (t)-[:tag]->(h))"
                        "FOREACH (val IN tweet.urls | MERGE (url:url) on create SET url.id=val MERGE (t)-[:include]->(url))"
                        "FOREACH (val IN tweet.medias | MERGE (m:media) on create SET  m.id=val MERGE (t)-[:has]->(m))"
                        "FOREACH (val IN tweet.user_mentions | MERGE (u1:user)  on create SET u1.id=val MERGE (t)-[:mention]->(u1)) "
                        "RETURN 'User: '+ u.id + ' sent '+ 'tweet: '+ t.id ", tweets=tweets)
        return result


if __name__ == "__main__":
    graphModel = GraphDbModel("bolt://localhost:7687", "neo4j", "test", 1)
    tweet1 = {'id': 3, 'userId': '1', 'locationId': 'l1', 'placeId': 'p1', 'hashtags': [], 'urls': [], 'medias': [],
              'user_mentions': []}
    tweet2 = {'id': 4, 'userId': '2', 'locationId': 'l2', 'placeId': 'p2', 'hashtags': [], 'urls': [], 'medias': [],
              'user_mentions': []}
    tweets = [tweet1, tweet2]
    graphModel.insert(tweets)
    graphModel.close()
