#!/usr/bin/env python
# encoding: utf-8

import tweepy
import csv
from datetime import date, datetime
import pandas as pd

# Twitter API credentials
consumer_key = "CRp24sWA9VRSVEBK7vLzDuezb"
consumer_secret = "AOEizPaqxxuY0zDqM3VNXTlSLmjArdR8xmC6VLysfymzhB4A1x"
access_key = "3176539950-H8T72Oqr4K8JtDrtDqnEffgElrEriIRckU9AZFZ"
access_secret = "h28tZlqQYqa9FufnPtoTcCq950zQahkESZUkJlHB3A6gh"


def get_all_tweets(screen_name):
    # hint:Twitter only allows access to a users most recent 3240 tweets with this method

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)

    # save most recent tweets
    alltweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    # keep grabbing tweets until reach the date limit.
    while len(new_tweets) > 0:
        print("getting tweets before %s" % (oldest))

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)

        # save most recent tweets
        alltweets.extend(new_tweets)

        # update the id of the oldest tweet
        oldest = alltweets[-1].id - 1

        print("...%s tweets downloaded so far" % (len(alltweets)))

        loop_label = 0
        earliest_limit = datetime(2017, 1, 20, 0, 0, 0)

        for tweet in new_tweets:
            raw_date = tweet.created_at
            if raw_date < earliest_limit:
                loop_label = 1
            else:
                continue
        if loop_label == 1:
            break




    # transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text] for tweet in alltweets]

    # write the csv, see to encoding method.
    with open('%s_tweets.csv' % screen_name, 'w', encoding='GB18030') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "created_at", "text"])
        writer.writerows(outtweets)

    pass
    print("Done with %s" % screen_name)



if __name__ == '__main__':
    # pass in the @username of the account you want to download
    get_all_tweets("elonmusk")
