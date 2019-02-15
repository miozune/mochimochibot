# -*- coding: utf-8 -*-

from tsae import StreamingEmulate
import tweepy
from Library import *

list_name = 'mochi'
auth = get_auth.get_auth()
api = tweepy.API(auth)
my_status = api.me()


def callback(status):
    reply_mochi = tweet_mochi.TweetMochi(status)

    if reply_mochi.is_reply_target(my_status):
        success = False

        try:
            api.update_status(reply_mochi.tweet(), status.id)
        except tweepy.error.TweepError as e:
            reply_mochi.reply_fail_report(e)

        try:
            api.create_favorite(status.id)
            success = True
        except tweepy.error.TweepError as e:
            reply_mochi.fav_fail_report(e)

        if success:
            reply_mochi.reply_and_fav_success_report()


def main():
    StreamingEmulate(api, list_name, callback).run()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n\nterminated by KeyboardInterrupt\n')
        import sys
        sys.exit()
