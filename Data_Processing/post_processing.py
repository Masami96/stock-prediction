import pandas as pd
import os
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer

Analyzer = SentimentIntensityAnalyzer()


def com_score(row):
    text = row['text']
    sentiment = Analyzer.polarity_scores(text)
    com_score = sentiment['compound']

    return com_score


def pos_score(row):
    text = row['text']
    sentiment = Analyzer.polarity_scores(text)
    pos_score = sentiment['pos']


    return pos_score


def neg_score(row):
    text = row['text']
    sentiment = Analyzer.polarity_scores(text)

    neg_score = sentiment['neg']

    return neg_score


def price_main_df(stock):

    price_df = load_price_pd(stock)

    df = price_df[['Company', 'Date', 'Open', 'Adj Close', 'Volume', 'Trend']]

    return df


def tweets_sent_df(stock):
    '''
    :param : str
    :return : create sentiment_matrix for stock
    '''

    tweets_df = load_tweets_pd(stock)


    # add new columns to dataframe
    tweets_df['com_score'] = tweets_df.apply(lambda row: com_score(row), axis=1)
    tweets_df['pos_score'] = tweets_df.apply(lambda row: pos_score(row), axis=1)
    tweets_df['neg_score'] = tweets_df.apply(lambda row: neg_score(row), axis=1)


    # create list containing all unique dates, and other lists we need to create a new DATAFRAME: SENTIMENT_MATRIX
    date_list = tweets_df['Date'].unique()

    date_count = []

    avg_com_scores, avg_pos_scores, avg_neg_scores = [], [], []

    for date in date_list:

        data_slice = tweets_df[tweets_df['Date'] == date]

        date_elm_count = data_slice.count()[0]

        date_count.append(date_elm_count)

        avg_com_scores.append(data_slice["com_score"].mean())
        avg_pos_scores.append(data_slice["pos_score"].mean())
        avg_neg_scores.append(data_slice["neg_score"].mean())

    sen_df = pd.DataFrame({
            'Company':[stock] * len(avg_com_scores),
            'Date': date_list,
            'count': date_count,
            'com_score': avg_com_scores,
            'pos_score': avg_pos_scores,
            'neg_score': avg_neg_scores})
    return sen_df


def save_sen_df_to_csv():
    stocks = ["AMZN","AAPL","TSLA","TWTR"]

    for stock in stocks:
        print("Creating {} Data Matrix".format(stock))
        price_df = price_main_df(stock)
        tweets_df = tweets_sent_df(stock)
        df = pd.merge(price_df, tweets_df, on=['Company','Date'])
        df.to_csv("DataMatrix/{}_DataMatrix.csv".format(stock))


def load_price_pd(stock):
    """
    :param  stock str:
    :return dataframes of price:
    """
    cwd = os.getcwd()
    price_all_files = os.listdir(os.path.join(cwd, 'price'))
    price_files = [os.path.join(cwd, 'price', file) for file in price_all_files if
                   file[:len(stock)] == stock]

    price_dfs = [pd.read_csv(file, encoding="ISO-8859-1") for file in price_files]

    if len(price_dfs) == 1:
        price_df = price_dfs[0]
    elif len(price_dfs) == 0:
        return "No price file for {}".format(stock)
    else:
        price_df = pd.concat(price_dfs, ignore_index=True)

    return price_df


def load_tweets_pd(stock):
    """
    :param  stock str:
    :return dataframes of tweets:
    """
    cwd = os.getcwd()
    tweets_all_files = os.listdir(os.path.join(cwd, 'tweets'))
    tweets_files = [os.path.join(cwd, 'tweets', file) for file in tweets_all_files if
                    file[:len(stock)] == stock]
    tweets_dfs = [pd.read_csv(file, encoding="ISO-8859-1") for file in tweets_files]

    if len(tweets_dfs) == 1:
        tweets_df = tweets_dfs[0]
    elif len(tweets_dfs) == 0:
        return "No tweets file for {}".format(stock)
    else:
        tweets_df = pd.concat(tweets_dfs, ignore_index=True)

    return tweets_df


if __name__ == '__main__':

    save_sen_df_to_csv()


