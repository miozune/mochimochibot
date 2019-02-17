# -*- coding: utf-8 -*-

import datetime
import random
from random import choice
from tsae import StreamingEmulate
import tweepy

import mochimochi
import setting
import utils

list_name = 'mochi'
api = setting.get_api()
my_status = api.me()


def callback(status):
    def count_mochi_num():
        text = status.text
        for word in mochimochi.ignore_words:
            text = text.replace(word, '')
        count = 0
        for mochi in ['モチ', 'もち', 'ﾓﾁ']:
            count += text.count(mochi)
        return count

    def is_reply_target():
        if (not status.retweeted) and ('RT @' not in status.text) \
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

    def generate_special_mochi():
        text = status.text
        special_mochi = []
        sp_count = 0
        for mochi in mochimochi.special_mochi:
            if text.count(mochi['name']) and random.random() < mochi['rate']:
                special_mochi.append(mochi['reply'])
                sp_count += text.count(mochi['name'])
        return special_mochi, sp_count

    def generate_raw_reply():
        count = count_mochi_num()
        special_mochi, sp_count = generate_special_mochi()
        count -= sp_count

        if count == 0:
            if sp_count == 0:
                normal_mochi = [choice(mochimochi.level1 + mochimochi.level2)]
            else:
                normal_mochi = []
        elif count == 1:
            normal_mochi = [choice(mochimochi.level1 + mochimochi.level2)]
        elif 2 <= count <= 5:
            normal_mochi = [choice(mochimochi.level1 + mochimochi.level2) for _ in range(count // 2 + 1)]
        elif 6 <= count <= 20:
            normal_mochi = [choice(mochimochi.level1 + mochimochi.level2 + mochimochi.level3)
                            for _ in range(count // 2 + 1)]
        else:
            normal_mochi = [choice(mochimochi.level1 + mochimochi.level2 + mochimochi.level3 + mochimochi.level4)
                            for _ in range(20)]

        return ''.join(special_mochi + normal_mochi)

    def reply_success_report(reply):
        print(datetime.datetime.now())
        print('{} @{}'.format(status.user.name, status.user.screen_name))
        print(status.text)
        print('->')
        print(reply)
        print('-' * 30)

    def reply_fail_report(reply, err):
        print('*' * 30)
        print('ERROR!: failed to tweet')
        print(reply)
        print(err)
        print('*' * 30)

    if is_reply_target():
        to_reply = '@{}\n'.format(status.user.screen_name)
        raw_reply = generate_raw_reply()
        reply = utils.trim(to_reply + raw_reply)
        try:
            api.update_status(reply, status.id)
            reply_success_report(reply.split('\n')[1])
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
