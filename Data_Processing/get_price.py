# from yahoo_finance import Share
# import pandas as pd
# tesla = Share('TSLA')
# history = tesla.get_historical('2017-2-27','2017-10-28')
#
# tesla_df = pd.DataFrame(tesla)
# tesla_df.to_csv('tesla_stock_data_yahoo.csv')

from pandas_datareader import data
import pandas as pd
from datetime import date
import os


def label_trend(row):
    if row['Adj Close'] - row['Open'] > 0:
        return 1
    else:
        return 0

date = "2017-10-1"
to_date = "2017-11-26"

stocks = ["AMZN","AAPL","TSLA","TWTR"]

for stock in stocks:

    print("query stock price data for {}".format(stock))

    tesla = data.DataReader(stock,'yahoo',date,to_date)
    tesla_df = pd.DataFrame(tesla)
    tesla_labeled = tesla_df.copy()

    tesla_labeled['Trend'] = tesla_labeled.apply(lambda row: label_trend(row), axis=1)

    tesla_labeled['Company'] = stock


    # rearrange the order of columns:
    cols = tesla_labeled.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    tesla_labeled = tesla_labeled[cols]



    # or dp.apply(label_trend, axis=1)

    cwd = os.getcwd()


    dir_path = os.path.join(cwd, 'price')
    file_name = '{}_price_{}-{}.csv'.format(stock, date, to_date)

    tesla_labeled.to_csv(os.path.join(dir_path, file_name))