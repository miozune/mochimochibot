# -*- coding: utf-8 -*-

import tweepy
from time import sleep
from Library import *

auth = get_auth.get_auth()
api = tweepy.API(auth)
my_status = api.me()


def main():
    friends_ids = []
    for friend_id in tweepy.Cursor(api.friends_ids, user_id=my_status.id).items():
        friends_ids.append(friend_id)

    followers_ids = []
    for follower_id in tweepy.Cursor(api.followers_ids, user_id=my_status.id).items():
        followers_ids.append(follower_id)

    not_following_ids = list(set(followers_ids) - set(friends_ids))

    if len(not_following_ids) == 0:
        sleep(70)
        exit()

    for i in range(0, len(not_following_ids), 100):
        for user in api.lookup_users(user_ids=not_following_ids[i:i + 100]):
            try:
                api.create_friendship(user.id)
                print('created friendship with ' + user.name + " @" + user.screen_name)

            except tweepy.error.TweepError as e:
                print('*' * 20)
                print('ERROR!: could not create friendship with @{0}, id:{1}'.format(user.name, user.id))
                print('error_status: ' + str(e))
                print('*' * 20)

                with open('Library\dump.csv', 'a') as f:
                    import csv
                    from datetime import datetime
                    writer = csv.writer(f)

                    writer.writerow(str(datetime.now()))
                    writer.writerow(str(e))
                    writer.writerow('-' * 30)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n\nterminated by KeyboardInterrupt\n')
        import sys
        sys.exit()
