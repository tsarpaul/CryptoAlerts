import os


# TODO store this somewhere persistent
class LastTweetID:
    __last_tweet_id_path = os.path.join(os.path.dirname(__file__), "last_tweet_id.txt")

    @classmethod
    def get(cls):
        with open(cls.__last_tweet_id_path, 'r') as f:
            last_tweet_id = f.read()
        return last_tweet_id

    @classmethod
    def update(cls, last_tweet_id):
        with open(cls.__last_tweet_id_path, 'w') as f:
            f.write(str(last_tweet_id))
