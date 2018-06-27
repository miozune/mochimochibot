# -*- coding: utf-8 -*-


def get_auth():
    import setting
    import tweepy

    auth = tweepy.OAuthHandler(setting.CONSUMER_KEY, setting.CONSUMER_SECRET)
    auth.set_access_token(setting.ACCESS_TOKEN, setting.ACCESS_SECRET)
    return auth
