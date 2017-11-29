from twitterscraper import query_tweets
from langdetect import detect
import os

search_list = ["TSLA",'AAPL','TWTR', 'AMZN']
from_date = "2017-10-1"
to_date = "2017-11-26"

for stock in search_list:

    print("Processing {}".format(stock))


    # Advance Search for each stock ------------- https://twitter.com/search-advanced
    # usage ---------- https://github.com/taspinar/twitterscraper
    # search by hashtags : #TSLA, #AAPL, #TWTR, #AMZN
    search_stock = "%23{}%20since%3A{}%20until%3A{}".format(stock, from_date, to_date)

    # query data
    list_of_tweets = query_tweets(search_stock, limit=None)

    print("Completing tweets query for {}".format(stock))

    cwd = os.getcwd()
    dir_path = os.path.join(cwd, 'tweets')
    output_file = stock + "_tweets_" + from_date + "-" + to_date + '.csv'
    file_path = os.path.join(dir_path, output_file)

    csv = open(file_path, 'bw')

    columnTitleRow = 'company,Date,text\n'
    csv.write(columnTitleRow.encode('gb18030'))

    for tweet in list_of_tweets:
        date = tweet.timestamp.strftime("%Y-%m-%d")

        text = tweet.text.replace("\"", "\"\"")

        lan = detect(text)
        try:
            if lan == 'en':

                row = stock + ',' + date + ',' + "\"" + text + "\"" + '\n'
                csv.write(row.encode('gb18030'))
        except Exception:
            print(Exception)