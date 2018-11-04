import requests

from src.collectors.twitter.twitter_api import generate_twitter_oauth1

if __name__ == "__main__":
    oauth1 = generate_twitter_oauth1()
    following = requests.get(
        "https://api.twitter.com/1.1/friends/list.json",
        params={
            "user_id": 849318396294463492,
            "cursor": -1,
            "include_user_entities": True,
            "count": 200
        },
        auth=oauth1
    )
    for followed in following.json()['users']:
        print("'{id}': {{'id': '{id}', 'name': '{name}'}}".format(id=followed['id_str'], name=followed['name']))
