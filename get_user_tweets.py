import pandas as pd
import snscrape.modules.twitter as sntwitter
import itertools
import os
import datetime
import config
import tweepy
import json

# Set up directory
maindir = os.getcwd()
outputdir = os.path.join(maindir,'Output')
followersdir = os.path.join(maindir,'Followers of accounts')

# Configure connection. Bearer token (Auth2.0) works for full archive.
client = tweepy.Client(bearer_token=config.bearer_token, wait_on_rate_limit= True)

# Loading dataset
users_file = pd.read_csv(os.path.join(followersdir,"Followers_England.csv"))
followers_id = users_file['follower_id']
followers_username = users_file['follower_username']

# Function to get tweets from a user account
def get_user_tweets(id, end_date):
    tweets = tweepy.Paginator(client.get_users_tweets, id=id, end_time=end_date)
    return tweets

for index,id in enumerate(followers_id):
    match_day = '2021-07-11'
    date_1 = datetime.datetime.strptime(match_day, '%Y-%m-%d')
    end_date = (date_1 + datetime.timedelta(days=2)).strftime('%Y-%m-%d')+str("T00:00:00Z")
    tweets = get_user_tweets(id,end_date)
    for i in tweets:
        print(i)