import re

from twython import TwythonStreamer

from twitter_api.api import *
from word_cloud import word_cloud


def analyze_streaming_twitter_data(output_file_name, count, track, language):
    oauth_token = SecureConfig.oauth_token
    oauth_token_secret = SecureConfig.oauth_token_secret
    if not (oauth_token and oauth_token_secret):
        twitter = Twython(consumer_key, consumer_secret)
        auth = twitter.get_authentication_tokens()
        auth_url = auth['auth_url']
        print(auth_url)
        verify_code = input()
        final_step = final_verify(oauth_verifier=verify_code, auth=auth)
        print(final_step)
        oauth_token = final_step.get("oauth_token")
        oauth_token_secret = final_step.get("oauth_token_secret")

    class MyStreamer(TwythonStreamer):
        def __init__(self, app_key, app_secret, oauth_token, oauth_token_secret):
            super().__init__(app_key, app_secret, oauth_token, oauth_token_secret)
            self.counter = 0

        def on_success(self, data):
            if 'text' in data:
                text = data['text']
                text = re.sub(r"RT @.*: ", '', text)
                text = re.sub(r"@\S+", '', text)
                text = re.sub(r"http\S+", '', text)
                text = re.sub(r"https\S+", '', text)
                print(text)
                with open(output_file_name, "a") as text_file:
                    text_file.write(text + "\n")
                self.counter += 1
                print(self.counter)
                if self.counter == count:
                    with open(output_file_name, "r") as f:
                        word_cloud(text=f.read())
                    self.disconnect()

        def on_error(self, status_code, data):
            print(status_code)
            print(data)
            self.disconnect()

    stream = MyStreamer(Config.consumer_key, Config.consumer_secret, oauth_token, oauth_token_secret)
    stream.statuses.filter(track=track, language=language, tweet_mode='extended')


analyze_streaming_twitter_data('iran.txt', 10, 'ایران', 'fa')
