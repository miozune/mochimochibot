# -*- coding: utf-8 -*-

import tweepy
from time import sleep
import setting

api = setting.get_api()
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
        # sleep(70)
        return

    for i in range(0, len(not_following_ids), 100):
        for user in api.lookup_users(user_ids=not_following_ids[i:i + 100]):
            try:
                api.create_friendship(user.id)
                print('created friendship with {} @{}'.format(user.name, user.screen_name))

            except tweepy.error.TweepError as e:
                print('*' * 20)
                print('ERROR!: could not create friendship with @{}, id:{}'.format(user.name, user.id))
                print('error_status: ' + str(e))
                print('*' * 20)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('terminated by user')
        import sys
        sys.exit()
