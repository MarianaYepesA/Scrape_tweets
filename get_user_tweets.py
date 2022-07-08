import pandas as pd
import os
import datetime
import config
import tweepy

# Set up directory
maindir = os.getcwd()
outputdir = os.path.join(maindir,'Output')
followersdir = os.path.join(maindir,'Followers of accounts')

# Configure connection. Bearer token (Auth2.0) works for full archive.
client = tweepy.Client(bearer_token=config.bearer_token_2, wait_on_rate_limit= True)

# Loading dataset
users_file = pd.read_csv(os.path.join(followersdir,"Followers_England.csv"))
followers_id = users_file['follower_id']
followers_username = users_file['follower_username']

# Function to get tweets from a user account
def get_user_tweets(id, end_date):
    tweets = tweepy.Paginator(client.get_users_tweets, id=id, end_time=end_date, tweet_fields=["lang","created_at","public_metrics","geo"],max_results=100).flatten(limit=1000)
    return tweets

results=[]
for index,id in enumerate(followers_id):
    match_day = '2021-12-31'
    date_1 = datetime.datetime.strptime(match_day, '%Y-%m-%d')
    end_date = (date_1).strftime('%Y-%m-%d')+str("T00:00:00Z")
    tweets = get_user_tweets(id, end_date)
    for tweet in tweets:
        if tweet.data is not None:
            print(tweet.lang, tweet.created_at, tweet.geo, tweet.public_metrics['retweet_count'],
                  tweet.public_metrics['reply_count'],
                  tweet.public_metrics['like_count'], tweet.public_metrics['quote_count'])
            results.append((id, followers_username[index],tweet.id, tweet.text,tweet.lang, tweet.created_at,tweet.geo,
                                tweet.public_metrics['retweet_count'],tweet.public_metrics['reply_count'],
                                tweet.public_metrics['like_count'],tweet.public_metrics['quote_count']))

tweets_results =pd.DataFrame(results, columns=['follower_id','follower_username','tweet_id','tweet_text','tweet_lang',
                                               'tweet_created_at','tweet_geo','tweet_retweet_count','tweet_reply_count',
                                               'tweet_like_count','tweet_quote_count'])

tweets_results.to_csv(os.path.join(outputdir,"Tweets_followers_England_2021.csv"), index=False)