#!/usr/bin/env python
import datetime

from twython import TwythonError

from specefic_tweet import get_twitter_user_rts_and_favs
from twitter_api.api import get_twitter_obj, get_rts_user_ids

from word_cloud import word_cloud

screen_name = 'faridebrahimi62'

tw = get_twitter_obj()

home_timeline = tw.get_user_timeline(screen_name=screen_name, tweet_mode='extended', count=50)

pure_user_tweet_ids = []
for tweet in home_timeline:
    tweet_id = tweet["id"]
    retweeted = tweet["retweeted"]
    if not retweeted:
        pure_user_tweet_ids.append(tweet_id)

text = ''
# for tweet_id in pure_user_tweet_ids:
#     ids = get_rts_user_ids(tw, tweet_id)
#     if ids:
#         for user_id in ids:
#             print(user_id)
#             print(type(user_id))
#             try:
#                 user = tw.show_user(user_id=user_id)
#                 screen_name = user["screen_name"]
#                 text += screen_name + ' '
#             except TwythonError as e:
#                 print(e)
#                 print(str(user_id))
#
# word_cloud(text)
rts_and_favs = get_twitter_user_rts_and_favs(screen_name, '1117417835838550018')
print(rts_and_favs)
# all_users_fav_users = []
# text = ''
# print(pure_user_tweet_ids)
# print(datetime.datetime.now())
# for tweet_id_str in pure_user_tweet_ids:
#     rts_and_favs = get_twitter_user_rts_and_favs(screen_name, str(tweet_id_str))
#     try:
#         favs = rts_and_favs[1]
#         rts = rts_and_favs[1]
#         all_users_fav_users.append(rts)
#         for user_id in rts:
#             user = tw.show_user(user_id=user_id)
#             name = user.get('screen_name')
#             name = name.replace(' ', '_')
#             text += name + ' '
#     except Exception:
#         pass
# print(datetime.datetime.now())
# print(text)
