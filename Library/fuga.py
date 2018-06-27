# -*- coding: utf-8 -*-

import tweepy
from . import get_auth

auth = get_auth.get_auth()
api = tweepy.API(auth)

api.create_friendship('12', follow=True)
