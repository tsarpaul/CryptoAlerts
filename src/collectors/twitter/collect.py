from .twitter_api import get_home_timeline
from .conf.last_tweet_id import LastTweetID
from .tweets import TweetAggregator


async def get_tweets_by_topics():
    last_tweet_id = LastTweetID.get()

    print("Getting home timeline since id {0}".format(last_tweet_id))
    response = await get_home_timeline(since_id=last_tweet_id)
    tweets = response.json()
    print("Collected {0} tweets".format(len(tweets)))
    if not tweets:
        return {}

    tweets_by_topics = TweetAggregator.aggregate_tweets(tweets)
    print("Tweets by topics:", tweets_by_topics)

    max_id_tweet = max(tweets, key=lambda tweet: tweet['id'])
    last_tweet_id = max_id_tweet['id_str']
    LastTweetID.update(last_tweet_id)

    return tweets_by_topics
