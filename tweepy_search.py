import tweepy
import config

client = tweepy.Client(bearer_token=config.bearer_token)

'''
Get 100 responses, tweets from Chile and using some hastags. No retweets considered


query = '#ChileKorea OR #Crisismigratoria OR #Migracion OR #ChilevsKorea OR #Laroja OR #Friendlymatch OR #BenBrereton OR #Brereton -is:retweet place_country:"CL" '
date_since = "2022-06-06"

response = client.search_recent_tweets(query=query,
                                       max_results=100,
                                       tweet_fields=['created_at','lang'],
                                       user_fields=['profile_image_url'],
                                       expansions=['author_id','geo.place_id'])

users = {u['id']:u for u in response.includes['users']}
places = {p['id']:p for p in response.includes['places']}

for tweet in response.data:
    print(tweet.geo)
    if tweet.geo:
        place = places[tweet.geo['place_id']]
        print(tweet.lang)
        print(place.full_name)
        
'''

# if you want more than a 100 tweets you do the following (say 1000, from anywhere and considering retweets):
query = '#ChileKorea OR #Crisismigratoria OR #Migracion OR #ChilevsKorea OR #Laroja OR #Friendlymatch OR #BenBrereton OR #Brereton '

file_name = 'tweets.txt'

with open(file_name, 'a+') as filehandler:
    for tweet in tweepy.Paginator(client.search_recent_tweets, query=query, max_results=100).flatten(limit=1000):
        print(tweet.text)
        print(tweet.lang)
        filehandler.write('%s\n' )
