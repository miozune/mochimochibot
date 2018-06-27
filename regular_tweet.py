# -*- coding: utf-8 -*-

import tweepy
from random import choice
from random import randint
from Library import *
from Library.tweet_mochi import shortened_text

auth = get_auth.get_auth()
api = tweepy.API(auth)


def regular_tweet():
    tweet = ''.join([choice(mochimochi.level1 + mochimochi.level2 + mochimochi.level3 + mochimochi.level4)
                    for _ in range(1, randint(1, 20))])
    tweet = shortened_text(tweet)
    api.update_status(tweet)
    print('regular tweet success!')
    print(tweet)
    print('-' * 20)
