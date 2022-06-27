import pandas as pd
import snscrape.modules.twitter as sntwitter
import itertools
import os
import datetime
import config
import tweepy
import json
from dateutil import relativedelta

# Set up directory
maindir = os.getcwd()
outputdir = os.path.join(maindir,'Output')

# Configure connection. Bearer token (Auth2.0) works for full archive.
client = tweepy.Client(bearer_token=config.bearer_token_2, wait_on_rate_limit=True)

def count_tweets_month(keyword, start, end, place):
    if place == "":
        count = client.get_all_tweets_count(query=keyword, granularity='day', start_time=start, end_time=end)
    else :
        count = client.get_all_tweets_count(query=keyword + str(' place_country:'+place), granularity='day', start_time=start, end_time=end)
    return count[0]

keywords = ['immigrant','migration','black']
places = ['','US','GB','IT','FR']
for k in keywords:
    for p in places:
        results = []
        starting_date = datetime.datetime.strptime('2021-01-01', '%Y-%m-%d')
        filename = "tweet_count_2021_" + str(k) + "_" + str(p) + ".csv"
        for single_date in (starting_date + relativedelta.relativedelta(months = n) for n in range(12)):
            print(filename)
            print(k, single_date.strftime('%Y-%m-%d') + str('T00:00:00Z'),
                  (single_date + relativedelta.relativedelta(months = 1)).strftime('%Y-%m-%d') + str('T00:00:00Z'), p)
            tweets_count = count_tweets_month(k, single_date.strftime('%Y-%m-%d') + str('T00:00:00Z'),
                                           (single_date + relativedelta.relativedelta(months = 1)).strftime('%Y-%m-%d') + str(
                                               'T00:00:00Z'), p)
            for count in tweets_count:
                results.append((k, p, count['start'], count['end'], count['tweet_count']))
        tweets_results = pd.DataFrame(results, columns=['Keyword', 'Place', 'Start_date', 'End_date', 'Tweets_count'])
        tweets_results.to_csv(os.path.join(outputdir, filename), index=False)