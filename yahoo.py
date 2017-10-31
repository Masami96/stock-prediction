# from yahoo_finance import Share
# import pandas as pd
# tesla = Share('TSLA')
# history = tesla.get_historical('2017-2-27','2017-10-28')
#
# tesla_df = pd.DataFrame(tesla)
# tesla_df.to_csv('tesla_stock_data_yahoo.csv')

from pandas_datareader import data
import pandas as pd


def label_trend(row):
    if row['Close'] - row['Open'] > 0:
        return 1
    else:
        return 0


tesla = data.DataReader('TSLA','yahoo','2017-2-14')
tesla_df = pd.DataFrame(tesla)
tesla_labeled = tesla_df.copy()
# tesla_test = tesla_df.copy()

tesla_labeled['Trend'] = tesla_labeled.apply(lambda row: label_trend(row), axis=1)

# or dp.apply(label_trend, axis=1)




# print(tesla_test)
tesla_labeled.to_csv('tesla_stock_data_labeled.csv')