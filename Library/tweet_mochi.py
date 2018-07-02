# -*- coding: utf-8 -*-

from . import mochimochi


def count_text_bytes(sentence):
    cumulative_sum = [0]
    for c in sentence:
        if 0 <= ord(c) <= 4351 or 8192 <= ord(c) <= 8205 or 8208 <= ord(c) <= 8223 or 8242 <= ord(c) <= 8247:
            cumulative_sum.append(cumulative_sum[-1] + 1)
        else:
            cumulative_sum.append(cumulative_sum[-1] + 2)
    del cumulative_sum[0]
    return cumulative_sum


def shortened_text(sentence):
    from bisect import bisect_right
    return sentence[:bisect_right(count_text_bytes(sentence), 280)]


class TweetMochi(object):
    def __init__(self, status):
        self.status = status
        self.text = status.text
        self.screen_name = status.user.screen_name
        self.username = status.user.name
        self.instance_tweet = None

    def mochi_num(self):
        _text = self.text
        for word in mochimochi.ignore_words:
            _text = self.text.replace(word, "")

        count = 0
        for mochi in ["モチ", "もち", "ﾓﾁ"]:
            count += _text.count(mochi)
        return count

    def is_reply_target(self, my_status):
        if (not self.status.retweeted) and ("RT @" not in self.text) \
                and self.status.user.id != my_status.id \
                and ((self.status.in_reply_to_user_id is None and self.mochi_num() > 0)
                     or self.status.in_reply_to_user_id == my_status.id):
            # RTには反応しない
            # 自身のツイートには反応しない
            # リプじゃなければモチが含まれていること
            # リプならすべて反応、ただし自分以外へのリプには巻き込みモチしない
            return True
        else:
            return False

    def raw_reply_tweet(self):
        from random import choice
        to_reply = '@{0}\n'.format(self.screen_name)
        count = self.mochi_num()

        if count <= 1:
            return to_reply + choice(mochimochi.level1)
        elif 2 <= count <= 5:
            return to_reply + ''.join([choice(mochimochi.level1 + mochimochi.level2) for _ in range(count // 2)])
        elif 6 <= count <= 20:
            return to_reply + ''.join([choice(mochimochi.level1 + mochimochi.level2 + mochimochi.level3)
                                       for _ in range(count // 2)])
        else:
            return to_reply + ''.join([choice(mochimochi.level1 + mochimochi.level2 + mochimochi.level3 +
                                              mochimochi.level4) for _ in range(1, 20)])

    def tweet(self):
        self.instance_tweet = shortened_text(self.raw_reply_tweet())
        return self.instance_tweet

    def reply_and_fav_success_report(self):
        print('{0} @{1}'.format(self.username, self.screen_name))
        print(self.text)
        print('->')
        print(self.instance_tweet)
        print('-' * 20)

    def reply_fail_report(self, error_status):
        print('*' * 20)
        print('ERROR!: failed to tweet')
        print(self.instance_tweet)
        print('*' * 20)

        with open('dump.csv', 'a') as f:
            import csv
            from datetime import datetime
            writer = csv.writer(f)

            writer.writerow(str(datetime.now()))
            writer.writerow(str(error_status))
            writer.writerow(self.instance_tweet)
            writer.writerow('-' * 30)

    def fav_fail_report(self, error_status):
        print('*' * 20)
        print('ERROR!: failed to fav')
        print(self.status.text)
        print('*' * 20)

        with open('dump.csv', 'a') as f:
            import csv
            from datetime import datetime
            writer = csv.writer(f)

            writer.writerow(str(datetime.now()))
            writer.writerow(str(error_status))
            writer.writerow(self.status.text)
            writer.writerow('-' * 30)
