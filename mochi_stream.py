# -*- coding: utf-8 -*-

from bisect import bisect_right
import datetime
from random import choice
from tsae import StreamingEmulate
import tweepy
from Library import *

list_name = 'mochi'
auth = get_auth.get_auth()
api = tweepy.API(auth)
my_status = api.me()


def callback(status):
    def count_mochi_num():
        text = status.text
        for word in mochimochi.ignore_words:
            text = text.replace(word, "")
        count = 0
        for mochi in ["モチ", "もち", "ﾓﾁ"]:
            count += text.count(mochi)
        return count

    def is_reply_target():
        if (not status.retweeted) and ("RT @" not in status.text) \
                and status.user.id != my_status.id \
                and ((status.in_reply_to_user_id is None and count_mochi_num() > 0)
                     or status.in_reply_to_user_id == my_status.id):
            # RTには反応しない
            # 自身のツイートには反応しない
            # リプじゃなければモチが含まれていること
            # リプならすべて反応、ただし自分以外へのリプには巻き込みモチしない
            return True
        else:
            return False

    def generate_raw_reply():
        count = count_mochi_num()
        if count <= 1:
            return choice(mochimochi.level1 + mochimochi.level2)
        elif 2 <= count <= 5:
            return ''.join([choice(mochimochi.level1 + mochimochi.level2) for _ in range(count // 2 + 1)])
        elif 6 <= count <= 20:
            return ''.join([choice(mochimochi.level1 + mochimochi.level2 + mochimochi.level3)
                                       for _ in range(count // 2 + 1)])
        else:
            return ''.join([choice(mochimochi.level1 + mochimochi.level2 + mochimochi.level3 +
                                              mochimochi.level4) for _ in range(20)])

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

    def reply_success_report(raw_reply):
        print(datetime.datetime.now())
        print('{} @{}'.format(status.user.name, status.user.screen_name))
        print(status.text)
        print('->')
        print(raw_reply)
        print('-' * 30)

    def reply_fail_report(reply, err):
        print('*' * 30)
        print('ERROR!: failed to tweet')
        print(reply)
        print(err)
        print('*' * 30)

    if is_reply_target():
        to_reply = '@{0}\n'.format(status.user.screen_name)
        raw_reply = generate_raw_reply()
        reply = trim(to_reply + raw_reply)
        try:
            api.update_status(reply, status.id)
            reply_success_report(raw_reply)
        except tweepy.error.TweepError as err:
            reply_fail_report(reply, err)


def main():
    StreamingEmulate(api, list_name, callback).run()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('terminated by user')
        import sys
        sys.exit()
