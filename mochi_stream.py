# -*- coding: utf-8 -*-

import tweepy
from Library import *

auth = get_auth.get_auth()
api = tweepy.API(auth)
my_status = api.me()


class Listener(tweepy.StreamListener):
    def on_status(self, status):
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

        return True

    def on_error(self, status_code):
        print('*' * 20)
        print('ERROR! status code: ' + str(status_code))
        print('*' * 20)

        with open('Library\dump.txt', 'a') as f:
            import csv
            from datetime import datetime
            writer = csv.writer(f)

            writer.writerow(str(datetime.now()))
            writer.writerow(str(status_code))
            writer.writerow('-' * 30)

        if status_code == '420':
            print('disconnecting...')
            return False

        return True


def main():
    listener = Listener()
    stream = tweepy.Stream(auth, listener, secure=True)
    stream.userstream(async=True)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n\nterminated by KeyboardInterrupt\n')
        import sys
        sys.exit()
