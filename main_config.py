import os

from secure_config import SecureConfig


class Config:
    twitter_status_link = os.environ.get('TWITTER_STATUS_LINK', 'https://twitter.com/statuses/{}')
    consumer_key = os.environ.get('CONSUMER_KEY', SecureConfig.consumer_key)
    consumer_secret = os.environ.get('CONSUMER_SECRET', SecureConfig.consumer_secret)
    tweet_count = int(os.environ.get('TWEET_COUNT', 3))
