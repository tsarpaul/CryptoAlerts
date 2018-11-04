import datetime
import asyncio
import traceback

from .collect import get_tweets_by_topics


async def run_twitter(pub_client):
    twitter_rate_limit = 80  # 1 request per 80 seconds
    while True:
        try:
            print("Running at: ", datetime.datetime.now())

            tweets_by_topics = await get_tweets_by_topics()
            for topic, tweets in tweets_by_topics.items():
                msg = '\n'.join(
                    ['{user}: {text}'.format(user=tweet.user['name'], text=tweet.text) for tweet in tweets])
                # Escape characters for Slack
                msg = msg.replace('&', '&amp').replace('<', '&lt').replace('>', '&gt')
                await pub_client.publish(topic, msg)

            print("Done at: ", datetime.datetime.now(), '\n')
            await asyncio.sleep(twitter_rate_limit)
        except Exception:
            traceback.print_exc()
            await asyncio.sleep(twitter_rate_limit)

