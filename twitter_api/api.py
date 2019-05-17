import random
import time

from twython import Twython, TwythonError
from main_config import Config
import logging

from secure_config import SecureConfig

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


def get_twitter_obj():
    oauth_token = SecureConfig.oauth_token
    oauth_token_secret = SecureConfig.oauth_token_secret
    if not (oauth_token and oauth_token_secret):
        auth = get_verify_link()
        auth_url = auth['auth_url']
        print(auth_url)
        verify_code = input()
        final_step = final_verify(oauth_verifier=verify_code, auth=auth)
        print(final_step)
        oauth_token = final_step.get("oauth_token")
        oauth_token_secret = final_step.get("oauth_token_secret")
    twitter = Twython(consumer_key, consumer_secret, oauth_token, oauth_token_secret)
    return twitter


def get_rts_user_ids(twitter, tweet_id):
    all_ids = []
    cursor = -1
    while cursor != 0:
        try:
            retweeters_ids = twitter.get_retweets(id='1117417835838550018')
            cursor = retweeters_ids["next_cursor"]
            ids = retweeters_ids["ids"]
            all_ids += ids
        except TwythonError as e:
            print(e.error_code)
            raise
        if cursor:
            s = random.randint(55, 65)
            time.sleep(s)
    return all_ids
