import pandas as pd
import snscrape.modules.twitter as sntwitter
import itertools
import os
import datetime
import config
import tweepy
import json


# Configure connection. Bearer token (Auth2.0) works for full archive.
client = tweepy.Client(bearer_token=config.bearer_token, wait_on_rate_limit= True)

# Loading dataset
matches = pd.read_excel("Eurocupsf.xlsx")
#Separate teams in different columns
matches["Team 1"]=matches['Team 1'].astype(str)
matches["Team 2"]=matches['Team 2'].astype(str)

#Cleaning countries names
matches['Team 1'].replace({'Israel -':'Israel','Andorra -':'Andorra','Israel - Belgium':'Israel','Cyprus -':'Cyprus',
                            'Netherlands -':'Netherlands','Croatia -':'Croatia','Slovakia -':'Slovakia',
                            'Austria -':'Austria','North Macedonia -':'Macedonia','North Macedonia':'Macedonia',
                            'Kazakhstan -':'Kazakhstan','Belgium -':'Belgium','England -':'England',
                            'Luxembourg -':'Luxembourg','Portugal -':'Portugal','Albania -':'Albania',
                            'Moldova -':'Moldova','Wales -':'Wales','Georgia -':'Georgia','Gibraltar -':'Gibraltar',
                            'Sweden -':'Sweden','Italy -':'Italy','Hungary -':'Hungary','Poland -':'Poland',
                            'Slovenia -':'Slovenia','San Marino -':'San Marino','Kosovo -':'Kosovo',
                            'Montenegro -':'Montenegro','Turkey -':'Turkey','France -':'France','Ireland -':'Ireland',
                            'Switzerland -':'Switzerland','Norway -':'Norway','Romania -':'Romania','Armenia -':'Armenia',
                            'Estonia -':'Estonia','Belarus -':'Belarus','Azerbaijan -':'Azerbaijan','Iceland -':'Iceland',
                            'Scotland -':'Scotland','Finland -':'Finland','Bulgaria -':'Bulgaria','Serbia -':'Serbia',
                            'Ukraine -':'Ukraine','Denmark -':'Denmark','Malta -':'Malta','Latvia -':'Latvia',
                            'Germany -':'Germany','Russia -':'Russia','Greece -':'Greece','Lithuania -':'Lithuania',
                            'Spain -':'Spain','Bosnia-Herzegovina -':'Bosnia-Herzegovina','Czech':'Czech Republic',
                            'Northern':'Northern Ireland','Malta - Faroe':'Malta','Russia - San':'Russia',
                            'Israel - North':'Israel','Kosovo - Czech':'Kosovo','Spain - Faroe':'Spain',
                            'Belgium - San':'Belgium','Poland - North':'Poland','Scotland - San':'Scotland',
                            'Norway - Faroe':'Norway','Austria - North':'Austria','Sweden - Faroe':'Sweden',
                            'Georgia - North':'Georgia','North':'Macedonia',}, inplace=True)

matches['Team 2'].replace({'BosniaHerzegovina':'Bosnia-Herzegovina','Republic  Netherlands':'Netherlands','01':'Belgium',
                           'Ireland  Faroe Islands':'Faroe Islands','Ireland  Finland':'Finland','Ireland  Romania':'Romania',
                           'Ireland  Hungary':'Hungary','Ireland  Greece':'Greece','Ireland  Estonia':'Estonia',
                           'Islands':'Faroe Islands','Ireland  Belarus':'Belarus','North Macedonia':'Macedonia',
                           'Marino':'San Marino','Macedonia  Austria':'Austria','Republic':'Czech Republic',
                           'Ireland  Germany':'Germany','Macedonia  Slovenia':'Slovenia','Macedonia  Israel':'Israel',
                           'Macedonia  Kosovo':'Kosovo','Ireland  Slovakia':'Slovakia','Ireland  Netherlands':'Netherlands'}, inplace=True)

#Drop empty fields
matches.dropna()

#Import dictionary with capitals
with open('capitales.json', 'r') as JSON:
       json_dict = json.load(JSON)
capitals={}
for i in range(len(json_dict)):
    capitals[json_dict[i]["country"]]=json_dict[i]["city"]
capitals.update({'Luxembourg': 'Luxembourg'})

#Import dictionary with acronyms
acronyms = pd.read_csv('Acronyms.csv')
acronyms_dict = {}
for index,country in enumerate(acronyms['Country']):
    acronyms_dict[country] = acronyms['Acronym'][index]

#Assign capitals and acronyms to countries
for i in range(len(matches["Team 1"])):
    matches["capitals1"] = matches["Team 1"].apply(lambda x: capitals.get(x))
    matches["acronym1"] = matches["Team 1"].apply(lambda x: acronyms_dict.get(x))
for i in range(len(matches["Team 2"])):
    matches["capitals2"] = matches["Team 2"].apply(lambda x: capitals.get(x))
    matches["acronym2"] = matches["Team 2"].apply(lambda x: acronyms_dict.get(x))

#Drop empty fields
matches.dropna()

#Transform date into format for twitter
for i in range(len(matches["Date"])):
    matches["Date"][i]=datetime.datetime.strptime(matches["Date"][i].replace('_x000D_',''), "%d-%m-%Y").strftime("%Y-%m-%d")

# Get the number of tweets for a certain topic, get_all_tweets_count function access the full Archive.
keywords = ['immigrant', 'migration']

# Function to search tweet count for a certain keyword, date and place (place could be empty). It considers 2 days before
# and two after the match. The longest period it can consider is a month
def count_tweets(keyword, match_day, place):
    date_1 = datetime.datetime.strptime(match_day, '%Y-%m-%d')
    start_date = date_1 - datetime.timedelta(days=2)
    start = start_date.strftime('%Y-%m-%d') + str('T00:00:00Z')
    end_date = date_1 + datetime.timedelta(days=3)
    end = end_date.strftime('%Y-%m-%d') + str('T00:00:00Z')
    if place == "":
        count = client.get_all_tweets_count(query=keyword, granularity='day', start_time=start, end_time=end)
    else :
        count = client.get_all_tweets_count(query=keyword + str(' place_country:'+place), granularity='day', start_time=start, end_time=end)
    return count[0]

def count_tweets_all(keyword, match_day, place):
    date_1 = datetime.datetime.strptime(match_day, '%Y-%m-%d')
    start = date_1.strftime('%Y-%m-%d') + str('T00:00:00Z')
    end_date = datetime.date.today()
    end = end_date.strftime('%Y-%m-%d') + str('T00:00:00Z')
    if place == "":
        count = client.get_all_tweets_count(query=keyword, granularity='day', start_time=start, end_time=end)
    else :
        count = client.get_all_tweets_count(query=keyword + str(' place_country:'+place), granularity='day', start_time=start, end_time=end)
    return count[0]

results = []

for k in keywords:
    for place in ['','US','GB','FR','ES']:
        count_vector = count_tweets_all(k,'2022-05-01',place)
        for count in count_vector:
            results.append((k,place,count['start'],count['end'],count['tweet_count']))

tweets_count =pd.DataFrame(results, columns=['Keyword','Place','Start_date','End_date','Tweets_count'])
tweets_count.to_csv("Tweet_count_since_2019.csv", index=False)