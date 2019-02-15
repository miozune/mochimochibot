# -*- coding: utf-8 -*-

from bisect import bisect_right
import tweepy
from random import choice
from random import randint

import mochimochi
import setting

api = setting.get_api()


def count_text_bytes(sentence):
    cumulative_sum = [0]
    for c in sentence:
        if 0 <= ord(c) <= 4351 or 8192 <= ord(c) <= 8205 or 8208 <= ord(c) <= 8223 or 8242 <= ord(c) <= 8247:
            cumulative_sum.append(cumulative_sum[-1] + 1)
        else:
            cumulative_sum.append(cumulative_sum[-1] + 2)
    return cumulative_sum[1:]


def trim(sentence):
    return sentence[:bisect_right(count_text_bytes(sentence), 280)]


def regular_tweet():
    tweet = ''.join([choice(mochimochi.level1 + mochimochi.level2 + mochimochi.level3 + mochimochi.level4)
                    for _ in range(1, randint(2, 11))])
    tweet = trim(tweet)
    api.update_status(tweet)
    print('regular tweet success!')
    print(tweet)
    print('-' * 20)


def main():
    for count in range(5):
        try:
            regular_tweet()
            exit()
        except tweepy.error.TweepError:
                print('Warning: tweet duplicated: send again')
    print('ERROR!: failed regular tweet...')
