#!/usr/bin/env python3
import time
import tweepy
import operator

with open('consumerkey') as fp: consumer_key = fp.read().strip()
with open('consumersecret') as fp: consumer_secret = fp.read().strip()

with open('accesstoken') as fp: access_token = fp.read().strip()
with open('accesstokensecret') as fp: access_token_secret = fp.read().strip()

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# -----------------------------------------------------------------------------

def limit_handled(cursor):
    while True:
        try:
            yield next(cursor)
        except tweepy.RateLimitError:
            time.sleep(15*60)
        except StopIteration:
            break

myusers = []

for user in limit_handled(tweepy.Cursor(api.friends).items()):
    myusers.append((user.screen_name, user.status.created_at))
    print('$', len(myusers), end='\r', flush=True)
print()

myusers.sort(key=operator.itemgetter(1))

namelen = max(len(user[0]) for user in myusers)
for user in myusers:
    print('{:{namelen}s} : {}'.format(*user, namelen=namelen))
