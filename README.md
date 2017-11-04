# stock-prediction

1. Streaming folder contains codes of excuting crawling through live streaming.

2. Api_Search_keyword folder contains codes using api.search to get data roughly ~7 days ago and some tweets data from tesla, google and nvdia in json format.

3. Finish the code to crawl all tweets from one person ( and user-defined dates of tweets ).

4. Use yahoo_finance package or pandas built-in method to crawl stock prices data.



The .csv  files above include the stock price data of TESLA ( you can change to whatever you want ) and all tweets from the CEO of TESLA. I think it's much easier to deal with non-numeric classification so for stock price data each day I create the 'Trend' label to indicate price fluctuation.

Further attempts like crawling previous 4 days' tweets related to a specific company or it's products may be tried out.

I think it's more convenient for us to use some NLP packeges like TextBlob to do sentiment analysis on the tweets and get scores or labels about particular tweet rather than labeling them manually.


Feel free to convert .csv to .json.
