I should have tried tweepy.cursor to crawl but TweepyError(reach rate limits) always came up. So I turned to directly use original api.search() .
As to rate limits, I wrote some code to wait 15 mins when TweepyError comes up.
Use max_id and since_id to specify the range of dates we're gonna do crawling. get_id() takes the job to find max_id and since-id given the date paramters we want.
Data of each keyword we crawl will be respectivly stored into json files under the specified directories the code creates.

To narrow the number fo daily tweets we need to crawl, I try some constrains like location=USA in twitter_search() function.

Change the values of variables max_days_old and min_days_old in main section , you could specify the range of crawling dates(maximum maybe 8? I haven't tried)
