from twython import TwythonStreamer

from secure_config import SecureConfig
from twitter_api.api import *


class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
            print(data['text'])

    def on_error(self, status_code, data):
        print(status_code)

        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        # self.disconnect()


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

stream = MyStreamer(Config.consumer_key, Config.consumer_secret, oauth_token, oauth_token_secret)

try:
    result = stream.statuses.filter(track='دختر', language='fa')
    logger.info("success twitter api: ")
except TwythonError as e:
    logger.error(e.args)
