from .conf.twitter_users import twitter_users


class Tweet:
    __slots__ = ['id', 'user', 'text']

    def __init__(self, tweet_id, tweet_user_id, text):
        self.id = tweet_id
        self.user = twitter_users[tweet_user_id]  # Registered user
        self.text = text

    def __dict__(self):
        return {
            'id': self.id,
            'user': self.user,
            'text': self.text
        }


class TweetAggregator:
    @staticmethod
    def remove_retweeted_tweets(tweets):
        return filter(lambda tweet: not tweet.get('retweeted_status'), tweets)

    @staticmethod
    def remove_unregistered_users_tweets(tweets):
        return filter(lambda tweet: tweet['user']['id_str'] in twitter_users, tweets)

    @staticmethod
    def format_tweet(tweet):
        return Tweet(tweet['id'], tweet['user']['id_str'], tweet['text'])

    @staticmethod
    def group_tweets_to_topics(tweets):
        """Maps tweets to their respective registered user ids"""
        tweets_by_topics = {}
        for tweet in tweets:
            topic = tweet.user['topic']
            if topic not in tweets_by_topics:  # Initialize topic mapping
                tweets_by_topics[topic] = []
            tweets_by_topics[topic].append(tweet)
        return tweets_by_topics

    @classmethod
    def aggregate_tweets(cls, tweets):
        """Aggregate tweets to desired tweets to topic output"""
        tweets = cls.remove_unregistered_users_tweets(tweets)
        if not tweets:
            print("All tweet users were unregistered, skipping iteration")
            return {}

        tweets = cls.remove_retweeted_tweets(tweets)
        if not tweets:
            print("All tweets were retweeted, skipping iteration")
            return {}

        tweets = list(map(cls.format_tweet, tweets))

        tweets_to_topics = cls.group_tweets_to_topics(tweets)
        return tweets_to_topics
