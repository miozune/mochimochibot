# -*- coding: utf-8 -*-

from bisect import bisect_right
import tweepy
from random import choice
from random import randint

import mochimochi
import setting
import utils

api = setting.get_api()


def regular_tweet():
    tweet = ''.join([choice(mochimochi.level1 + mochimochi.level2 + mochimochi.level3 + mochimochi.level4)
                    for _ in range(1, randint(2, 11))])
    tweet = utils.trim(tweet)
    api.update_status(tweet)
    print('regular tweet success!')
    print(tweet)
    print('-' * 20)


def main():
    for _ in range(5):
        try:
            regular_tweet()
            return
        except tweepy.error.TweepError:
                print('Warning: tweet duplicated: send again')
    print('ERROR!: failed regular tweet...')
