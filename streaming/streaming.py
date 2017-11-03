from tweepy.streaming import StreamListener  # customise the way we process the incoming data.
from tweepy import OAuthHandler
from tweepy import Stream
import settings
import dataset

import csv
import json
import pandas as pd
import matplotlib.pyplot as plt

consumer_key ='CRp24sWA9VRSVEBK7vLzDuezb'
consumer_secret = 'AOEizPaqxxuY0zDqM3VNXTlSLmjArdR8xmC6VLysfymzhB4A1x'
access_token = '3176539950-H8T72Oqr4K8JtDrtDqnEffgElrEriIRckU9AZFZ'
access_token_secret = 'h28tZlqQYqa9FufnPtoTcCq950zQahkESZUkJlHB3A6gh'


# attempt to store our data into database (much easier for analyzing)
db = dataset.connect(settings.CONNECTION_STRING)


class StdOutListener(StreamListener):
    # global writer
    # writer = csv.writer(open('file.csv', 'a'))
    # writer.writerow(('Author', 'Date', 'Text'))

    def on_status(self, status):
        # return tweets that are not retweets (time saving).
        if hasattr(status,'retweeted_status'):
            return
        # if status.favorite_count is None or status.favorite_count < 10:
        #     return

        # get latent information we may need, but text and created_at are most important.
        # for more information: https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object
        description = status.user.description
        loc = status.user.location
        text = status.text
        coords = status.coordinates
        # geo = status.geo
        name = status.user.screen_name
        user_created = status.user.created_at
        followers = status.user.followers_count
        id_str = status.id_str
        created = status.created_at
        retweets = status.retweet_count

        print(created)
        print(text)
        # with open('fetched_tweets.txt', 'a',encoding='GB18030') as f:
        #     f.write('Author, Date, Text')
        #     writer = csv.writer(f)
        #     writer.writerow([status.author.screen_name, status.created_at, status.text])
        # writer.writerow(status.author.screen_name, status.created_at, status.text)
        table = db[settings.TABLE_NAME]
        table.insert(dict(
            user_description=description,
            user_location=loc,
            coordinates=coords,
            text=text,
            user_name=name,
            user_created=user_created,
            user_followers=followers,
            id_str=id_str,
            created=created,
            retweet_count=retweets,
        ))

    def on_error(self, status_code):
        if status_code == 420:
            return False


if __name__ == '__main__':

    # create a Stream object
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    # connect to twitter api using Stream.
    stream = Stream(auth, l)

    # this line filter Twitter Streams to capture data by the keywords and languages.
    stream.filter(languages=['en'], track=['tesla'])