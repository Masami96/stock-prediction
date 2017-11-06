import tweepy
from tweepy import OAuthHandler
import json
import datetime as dt
import time
import os
import sys


def api_load():
    consumer_key = 'CRp24sWA9VRSVEBK7vLzDuezb'
    consumer_secret = 'AOEizPaqxxuY0zDqM3VNXTlSLmjArdR8xmC6VLysfymzhB4A1x'
    access_token = '3176539950-H8T72Oqr4K8JtDrtDqnEffgElrEriIRckU9AZFZ'
    access_secret = 'h28tZlqQYqa9FufnPtoTcCq950zQahkESZUkJlHB3A6gh'
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    return tweepy.API(auth)

def write_tweets(tweets, filename):
    '''
    :param tweets:
    :param filename:
    :append tweets to a file
    '''
    with open(filename, 'a') as f:
        for tweet in tweets:
            json.dump(tweet._json, f)
            f.write('\n')

def twitter_search(api, query, since, until, lang, items_num):
        searched_tweets = []
    # while len(searched_tweets) < items_num:
        try:
            tweets = tweepy.Cursor(api.search,
                                       rpp=100,
                                       q=query,
                                       since=since,
                                       until=until,
                                       lang=lang).items()
            # print('found', len(tweets), 'tweets')
            if not tweets:
                print('no tweets')

                # break
            else:
                for tweet in tweets:
                    # just exclude the retweets that show up many times.
                    if not tweet.retweeted and 'RT @' not in tweet.text:
                            print(tweet.text)
            searched_tweets.extend(tweets)
        except tweepy.TweepError:
            print('tweets number limitation exception, 15min')
            print('(until:', dt.datetime.now()+dt.timedelta(minutes=15), ')')
            time.sleep(60*15)
            # break
        return searched_tweets



if __name__ =='__main__':
    '''
    search day and search keywords could be changed below.
    '''
    search_keywords = ['#nvidia']  # ['#tesla', '#google', '#nvidia']
    items_num = 1000

    since = '2017-10-31'
    until = '2017-11-1'
    min_days_old, max_days_old = 1, 2
    lang = 'en'

    for keyword in search_keywords:
        print('Now searching for: ',keyword)
        
        name = keyword.split()[0]
        json_file_root = name + '/' + name

        # create the folder to store json data.
        os.makedirs(os.path.dirname(json_file_root), exist_ok=True)
        
        # create the name of file with date.
        if max_days_old - min_days_old ==1:
            st = dt.datetime.now() - dt.timedelta(days=min_days_old)
            day = '{0}-{1:0>2}-{2:0>2}'.format(st.year, st.month, st.day)
        else:
            st1 = dt.datetime.now() - dt.timedelta(days=max_days_old-1)
            st2 = dt.datetime.now() - dt.timedelta(days=min_days_old)
            day = '{0}-{1:0>2}-{2:0>2}_to_{3}-{4:0>2}-{5:0>2}'.format(
                  st1.year, st1.month, st1.day, st2.year, st2.month, st2.day)

        # create the name of json file.
        json_file = json_file_root + '_' + day + '.json'

        if os.path.isfile(json_file):
            print('add tweets to file: ', json_file)

        api = api_load()

        exitcount = 0

        # loop for tweets crawling and writing to json file.
        while True:
            tweets = twitter_search(api, keyword, since,
                                            until, lang, items_num)
            # write tweets to the json file
            if tweets:
                write_tweets(tweets, json_file)
                exitcount = 0
            else:
                exitcount += 1
                if exitcount == 3:
                    if keyword == search_keywords[-1]:
                        sys.exit('Maximum number of empty tweet strings ---- exiting')
                    else:
                        print('Maximum number of empty tweet strings ----breaking')
                        break




