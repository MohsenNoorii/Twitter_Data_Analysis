from twython import Twython, TwythonError
from main_config import Config
import logging

consumer_key = Config.consumer_key
consumer_secret = Config.consumer_secret
logger = logging.getLogger()


def try_catch(func):
    def persist(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            logger.info("success twitter api: " + func.__name__)
            return result
        except TwythonError as e:
            logger.error(e.args)
            return False

    return persist


@try_catch
def get_verify_link():
    twitter = Twython(consumer_key, consumer_secret)
    auth = twitter.get_authentication_tokens()
    return auth


def final_verify(oauth_verifier, auth):
    twitter = Twython(consumer_key, consumer_secret, auth['oauth_token'], auth['oauth_token_secret'])
    try:
        final_step = twitter.get_authorized_tokens(oauth_verifier)
        return final_step
    except TwythonError as e:
        print(e.error_code)
        return False


def send_tweet_api(user, tweet_text):
    twitter = Twython(consumer_key, consumer_secret, user.oauth_token, user.oauth_token_secret)
    try:
        result = twitter.update_status(status=tweet_text)
        return result
    except TwythonError as e:
        print(e.error_code)
        return False


def home_time_line(user):
    twitter = Twython(consumer_key, consumer_secret, user.oauth_token, user.oauth_token_secret)
    try:
        result = twitter.get_home_timeline(count=Config.tweet_count, tweet_mode='extended')
        return result
    except TwythonError as e:
        print(e.error_code)
        return False


def search_api(user, query):
    twitter = Twython(consumer_key, consumer_secret, user.oauth_token, user.oauth_token_secret)
    try:
        result = twitter.search(q=query, count=Config.tweet_count, tweet_mode='extended')
        return result
    except TwythonError as e:
        print(e.error_code)
        return False
