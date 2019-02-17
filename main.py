# -*- coding: utf-8 -*-

from apscheduler.schedulers.blocking import BlockingScheduler

import auto_follow
import regular_tweet
import stream

schedule = BlockingScheduler()


@schedule.scheduled_job('interval', seconds=70)
def timed_auto_follow():
    auto_follow.main()


@schedule.scheduled_job('cron', hour='0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23')
def timed_regular_tweet():
    regular_tweet.main()


# @schedule.scheduled_job('interval', seconds=70)
# def timed_regular_tweet():
#     regular_tweet.regular_tweet()


if __name__ == '__main__':
    stream.main()
    schedule.start()
