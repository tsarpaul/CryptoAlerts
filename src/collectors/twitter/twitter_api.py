import asyncio

import requests
from requests_oauthlib import OAuth1

from .conf.twitter_auth import TwitterAuth


def generate_twitter_oauth():
    return OAuth1(
        TwitterAuth.consumer_key,
        TwitterAuth.consumer_secret,
        TwitterAuth.access_token,
        TwitterAuth.access_token_secret
    )


async def get_home_timeline(since_id):
    url = 'https://api.twitter.com/1.1/statuses/home_timeline.json'
    params = {
        'count': 200,
        'trim_user': False,
        'include_entities': True,
        'since_id': since_id
    }
    oauth1 = generate_twitter_oauth()
    tweets = requests.get(url=url, auth=oauth1, params=params)
    return tweets

