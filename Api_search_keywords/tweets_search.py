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
    with open(filename,'a') as f:
        for tweet in tweets:
            json.dump(tweet._json, f)
            f.write('\n')


def twitter_search(api, query, max_tweets, max_id, since_id, location):
    searched_tweets =[]
    while len(searched_tweets) < max_tweets:
        remaining_tweets = max_tweets - len(searched_tweets)
        try:
            tweets = api.search(q=query, count=remaining_tweets,
                                since_id=str(since_id),
                                max_id=str(max_id-1),
                                geocode=location)
            print('found', len(tweets), 'tweets')
            if not tweets:
                print('no tweets')
                break
            searched_tweets.extend(tweets)
            max_id=tweets[-1].id
        except tweepy.TweepError:
            print('tweets number limitation exception, 15min')
            print('(until:', dt.datetime.now()+dt.timedelta(minutes=15), ')')
            time.sleep(60*15)
            break
    return searched_tweets, max_id


def get_id(api, date='', days_ago=9, query='a'):
    if date:
        # return the id from the start fo the given day
        sd = date + dt.timedelta(days=1)
        tweet_date = '{0}-{1:0>2}-{2:0>2}'.format(sd.year, sd.month, sd.day)
        tweet = api.search(q=query, count=1, until=tweet_date)
    else:
        sd = dt.datetime.now() - dt.timedelta(days=days_ago)
        tweet_date = '{0}-{1:0>2}-{2:0>2}'.format(sd.year, sd.month, sd.day)
        tweet = api.search(q=query, count=1000, until=tweet_date)
        print('search to:', tweet[0].created_at)
    return tweet[0].id



if __name__ =='__main__':
    '''
    search day and search keywords could be changed below.
    '''
    search_keywords = ['#tesla', '#google', '#nvidia']
    max_tweets = 100 # max number of tweets per search
    min_days_old, max_days_old = 2, 7
    USA = '39.8,-95.583068847656,2500km'

    # loop for every keyword and create json file for each of them
    for keyword in search_keywords:
        print('Now searching for: ',keyword)
        name = keyword.split()[0]
        json_file_root = name + '/' + name
        os.makedirs(os.path.dirname(json_file_root), exist_ok=True)
        flg = False

        # open the file that stores tweets
        if max_days_old - min_days_old ==1:
            st = dt.datetime.now() - dt.timedelta(days=min_days_old)
            day = '{0}-{1:0>2}-{2:0>2}'.format(st.year, st.month, st.day)
        else:
            st1 = dt.datetime.now() - dt.timedelta(days=max_days_old-1)
            st2 = dt.datetime.now() - dt.timedelta(days=min_days_old)
            day = '{0}-{1:0>2}-{2:0>2}_to_{3}-{4:0>2}-{5:0>2}'.format(
                  st1.year, st1.month, st1.day, st2.year, st2.month, st2.day)
        json_file = json_file_root + '_' + day + '.json'
        if os.path.isfile(json_file):
            print('add tweets to file: ', json_file)
            flg = True

        # get authorization from API
        api = api_load()

        if flg is True:
            # open the json file and get latest tweet id
            with open(json_file, 'r') as f:
                lines = f.readline()
                max_id = json.loads(lines[-1]['id'])
                print('Searching from the bottom id')
        else:
            if min_days_old == 0:
                max_id = -1
            else:
                    max_id = get_id(api, days_ago=(min_days_old - 1))

        # set the smallest id to search for
        since_id = get_id(api, days_ago=(max_days_old - 1))
        print('starting point(id)=', max_id)
        print('ending point(id)=', since_id)


        # query for tweets
        exitcount = 0
        while True:
            tweets, max_id = twitter_search(api, keyword, max_tweets,
                                            max_id=max_id, since_id=since_id, location=USA)
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
















