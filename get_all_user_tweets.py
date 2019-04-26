#!/usr/bin/env python

from secure_config import SecureConfig
from specefic_tweet import get_twitter_user_rts_and_favs
from twitter_api.api import *
from persian_wordcloud.wordcloud import PersianWordCloud, add_stop_words
from wordcloud import STOPWORDS as EN_STOPWORDS
from os import path
from PIL import Image
import numpy as np

d = path.dirname(__file__)
screen_name = 'real_dr_b'


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
home_timeline = twitter.get_user_timeline(screen_name=screen_name, tweet_mode='extended', count=50)

tweet_ids_list = []
for tweet in home_timeline:
    tweet_id = tweet.get('id')
    tweet_ids_list.append(tweet_id)
all_users_fav_users = []
text = ''

for tweet_id_str in tweet_ids_list:
    rts_and_favs = get_twitter_user_rts_and_favs(screen_name, str(tweet_id_str))
    try:
        favs = rts_and_favs[1]
        all_users_fav_users.append(favs)
        for user_id in favs:
            user = twitter.show_user(user_id=user_id)
            name = user.get('screen_name')
            name = name.replace(' ', '_')
            text += name + ' '
    except Exception:
        pass
print(text)

d = path.dirname(__file__)
twitter_mask = np.array(Image.open(path.join(d, "twitter-logo.jpg")))

stopwords = add_stop_words(['کاسپین'])
stopwords |= EN_STOPWORDS

# Generate a word cloud image

wordcloud = PersianWordCloud(
    only_persian=False,
    max_words=200,
    stopwords=stopwords,
    margin=0,
    width=800,
    height=800,
    min_font_size=1,
    max_font_size=500,
    random_state=True,
    background_color="white",
    mask=twitter_mask
).generate(text)

image = wordcloud.to_image()
image.show()
image.save('en-fa-result.png')
