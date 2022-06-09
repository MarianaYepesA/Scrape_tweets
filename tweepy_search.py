import tweepy
import config

# Configure connection. Bearer token (Auth2.0) works for full archive. If you want only recent tweets then Auth1.0 is
# enough with auth_keys
client = tweepy.Client(bearer_token=config.bearer_token)


# Get 100 responses, tweets from Chile and using some hashtags. No retweets considered
'''
query = '#ChileKorea OR #Crisismigratoria OR #Migracion OR #ChilevsKorea OR #Laroja OR #Friendlymatch OR #BenBrereton
        OR #Brereton -is:retweet place_country:"CL" '
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
'''
query = '#ChileKorea OR #Crisismigratoria OR #Migracion OR #ChilevsKorea OR #Laroja OR #Friendlymatch OR #BenBrereton' \
      ' OR #Brereton -is:retweet'

file_name = 'tweets.txt'

with open(file_name, 'a+', encoding="utf-8") as file_handler:
    for tweet in tweepy.Paginator(client.search_recent_tweets, query=query, max_results=100).flatten(limit=1000):
        print(tweet.text)
        print(tweet.lang)
        file_handler.write('%s\n' % tweet.text)
        file_handler.write('%s\n' % tweet.id)
'''

# Now we will use the full archive to access old tweets

query = '#ChileKorea OR #Crisismigratoria OR #Migracion OR #ChilevsKorea OR #Laroja OR #Friendlymatch OR #BenBrereton' \
      ' OR #Brereton -is:retweet place_country:US '

start_time = '2022-06-01T00:00:00Z'
end_time = '2022-06-03T00:00:00Z'

response = client.search_all_tweets(query=query, max_results=100, start_time=start_time, end_time=end_time)

file_name = 'tweets_old_US.txt'

with open(file_name, 'a+', encoding="utf-8") as file_handler:
    for tweet in tweepy.Paginator(client.search_recent_tweets, query=query, max_results=100).flatten(limit=1000):
        print(tweet.text)
        print(tweet.lang)
        file_handler.write('%s\n' % tweet.text)
        file_handler.write('%s\n' % tweet.id)
