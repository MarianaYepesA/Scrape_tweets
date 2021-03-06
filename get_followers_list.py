import pandas as pd
import snscrape.modules.twitter as sntwitter
import itertools
import os
import datetime
import config
import tweepy
import json
import math
import numpy as np

# Configure connection. Bearer token (Auth2.0) works for full archive.
client = tweepy.Client(bearer_token=config.bearer_token, wait_on_rate_limit= True)

# Loading dataset
teams = pd.read_csv("Twitter accounts national teams.csv")
team_accounts = [team.split("/")[-1] for team in teams['Twitter account football team (national)']]
team_accounts_english = [team.split("/")[-1] for team in teams['Twitter account football team (english)'] if team is not np.nan]

team_accounts_id = []

for team in team_accounts_english:
    team_accounts.append(team)

#function to get an account id, and its followers
def get_followers(account):
    id = client.get_users(usernames = account)[0][0]['id']
    for fol in tweepy.Paginator(client.get_users_followers, id=id, max_results=100, user_fields=["location","created_at"]).flatten(limit=10000):
        if fol.location is not None:
            results.append((account,id,fol['username'],fol['id'], fol.location, fol.created_at))
        else:
            results.append((account, id, fol['username'], fol['id'], "", fol.created_at))

for account in team_accounts:
    results = []
    followers = get_followers(account)
    followers_team =pd.DataFrame(results, columns=['account_name','account_id','follower_username','follower_id', 'follower_location','follower_created_at'])
    followers_team.to_csv(os.path.join(os.getcwd(),'Followers of accounts',"Followers_"+str(account)+".csv"), index=False)