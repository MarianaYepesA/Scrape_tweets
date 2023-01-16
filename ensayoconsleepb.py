#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 11:43:01 2022

@author: mariana
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 14:15:07 2022

@author: mariana
"""
#import all necessary packages

import pandas as pd
import snscrape.modules.twitter as sntwitter
import itertools
import os
import datetime

from pathlib import Path  
from textblob import TextBlob
import sys
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import nltk
import pycountry
import re
import string
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
from langdetect import detect
from nltk.stem import SnowballStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import squarify
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
import emoji    # removes emojis
import re   # removes links
import en_core_web_sm
import string
import itertools
import collections
from collections import Counter
import time
###########################################################
maindir = os.getcwd()
outputdir = os.path.join(maindir)

#Load tweets file
#tweets_file = pd.read_csv("2021-07-10+Italy_England+sinpalabras.csv")
#tweets = tweets_file['content']
### FUNCTIONS USED IN SCRIPT
import nltk
nltk.downloader.download('vader_lexicon')
nltk.download('wordnet')
nltk.download('omw-1.4')
#Function to calculate percentage
def percentage(part, whole):
  percentage = 100 * float(part)/float(whole)
  return percentage

#Function for count_values_in single columns
def count_values_in_column(data,feature):
 total=data.loc[:,feature].value_counts(dropna=False)
 percentage=round(data.loc[:,feature].value_counts(dropna=False,normalize=True)*100,2)
 return pd.concat([total,percentage],axis=1,keys=['Total','Percentage'])

#Function to Create Wordcloud, which
def create_wordcloud(text, filename):
 mask = np.array(Image.open('cloud.png'))
 stopwords = set(STOPWORDS)
 wc = WordCloud(background_color='white', mask = mask, max_words=300, stopwords=stopwords, repeat=True)
 wc.generate(str(text))
 wc.to_file(os.path.join(outputdir, str(filename)+'.png'))
 print('Word Cloud Saved Successfully')
 
def scrape_tweets(keyword,since,match): #llamar esta función para cada día
     date_1 = datetime.datetime.strptime(since, '%Y-%m-%d').date()
     dia_1= date_1.strftime('%Y-%m-%d')
     start_date = date_1 - datetime.timedelta(days=1)
     start = start_date.strftime('%Y-%m-%d')
     end_date = date_1 + datetime.timedelta(days=1)
     final = end_date.strftime('%Y-%m-%d')
     text=f"{keyword} since:{start} until:{final} "
     data = pd.DataFrame(itertools.islice(sntwitter.TwitterSearchScraper(
     text).get_items(), 5000))
     fechas=[start,date_1,final]
     try:
         data.to_csv(f"{since}+{match}.csv")
     except:
         data.to_csv(f"{since}+{match}.csv")
         
     return data


#begin scraping tweets

#Load Matches data
partidos=pd.read_excel("Eurocupsfdesde2010.xlsx")
#Separate teams in different columns
partidos["equipo 1"]=partidos['Team 1'].astype(str)
partidos["equipo 2"]=partidos['Team 2'].astype(str)

for s in partidos['equipo 1']:
    s.replace('_x000D_','')
#Cleaning countries names
partidos['equipo 1'].replace({'Israel -':'Israel',
                              'Andorra -':'Andorra',
                              'Israel - Belgium':'Israel',
                              'Cyprus -':'Cyprus',
                              'Netherlands -':'Netherlands',
                              'Croatia -':'Croatia',
                              'Slovakia -':'Slovakia',
                              'Austria -':'Austria',
                              'North Macedonia -':'Macedonia',
                              'North Macedonia':'Macedonia',
                              'Kazakhstan -':'Kazakhstan',
                              'Belgium -':'Belgium',
                              'England -':'England',
                              'Luxembourg -':'Luxembourg',
                              'Portugal -':'Portugal',
                              'Albania -':'Albania',
                              'Moldova -':'Moldova',
                              'Wales -':'Wales',
                              'Georgia -':'Georgia',
                              'Gibraltar -':'Gibraltar',
                              'Sweden -':'Sweden',
                              'Italy -':'Italy',
                              'Hungary -':'Hungary',
                              'Poland -':'Poland',
                              'Slovenia -':'Slovenia',
                              'San Marino -':'San Marino',
                              'Kosovo -':'Kosovo',
                              'Montenegro -':'Montenegro',
                              'Turkey -':'Turkey',
                              'France -':'France',
                              'Ireland -':'Ireland',
                              'Switzerland -':'Switzerland',
                              'Norway -':'Norway',
                              'Romania -':'Romania',
                              'Armenia -':'Armenia',
                              'Estonia -':'Estonia',
                              'Belarus -':'Belarus',
                              'Azerbaijan -':'Azerbaijan',
                              'Iceland -':'Iceland',
                              'Scotland -':'Scotland',
                              'Finland -':'Finland',
                              'Bulgaria -':'Bulgaria',
                              'Serbia -':'Serbia',
                              'Ukraine -':'Ukraine',
                              'Denmark -':'Denmark',
                              'Malta -':'Malta',
                              'Latvia -':'Latvia',
                              'Germany -':'Germany',
                              'Russia -':'Russia',
                              'Greece -':'Greece',
                              'Lithuania -':'Lithuania',
                              'Spain -':'Spain',
                              'Bosnia-Herzegovina -':'Bosnia-Herzegovina',
                              'Czech':'Czech Republic',
                              'Northern':'Northern Ireland',
                              'Malta - Faroe':'Malta',
                              'Russia - San':'Russia',
                              'Israel - North':'Israel',
                              'Kosovo - Czech':'Kosovo',
                              'Spain - Faroe':'Spain',
                              'Belgium - San':'Belgium',
                              'Poland - North':'Poland',
                              'Scotland - San':'Scotland',
                              'Norway - Faroe':'Norway',
                              'Austria - North':'Austria',
                              'Sweden - Faroe':'Sweden',
                              'Georgia - North':'Georgia',
                              'North':'Macedonia',}, inplace=True)
for i in partidos['equipo 2']:
    i.replace('_x000D_','')
partidos['equipo 2'].replace({'BosniaHerzegovina':'Bosnia-Herzegovina',
                              'Republic  Netherlands':'Netherlands',
                              '01':'Belgium',
                              'Ireland  Faroe Islands':'Faroe Islands',
                              'Ireland  Finland':'Finland',
                              'Ireland  Romania':'Romania',
                              'Ireland  Hungary':'Hungary',
                              'Ireland  Greece':'Greece',
                              'Ireland  Estonia':'Estonia',
                              'Islands':'Faroe Islands',
                              'Ireland  Belarus':'Belarus',
                              'North Macedonia':'Macedonia',
                              'Marino':'San Marino',
                              'Macedonia  Austria':'Austria',
                              'Republic':'Czech Republic',
                              'Ireland  Germany':'Germany',
                              'Macedonia  Slovenia':'Slovenia',
                              'Macedonia  Israel':'Israel',
                              'Macedonia  Kosovo':'Kosovo',
                              'Ireland  Slovakia':'Slovakia',
                              'Ireland  Netherlands':'Netherlands'}, inplace=True)


#Drop empty fields
partidos
partidos.dropna()



#Import dictionary with capitals
import json
with open('capitales.json', 'r') as JSON:
       json_dict = json.load(JSON)



#Import dictionary with acronyms
acronyms = pd.read_csv('Acronyms.csv')
acronyms_dict = {}
for index,country in enumerate(acronyms['Country']):
    acronyms_dict[country] = acronyms['Acronym'][index]


capitales={}
for i in range(len(json_dict)):
    capitales[json_dict[i]["country"]]=json_dict[i]["city"]



capitales.update({'Luxembourg': 'Luxembourg'})
capitales.values()



#Assign capitals and acronyms to countries
for i in range(len(partidos["equipo 1"])):
    partidos["capitales1"] = partidos["equipo 1"].apply(lambda x: capitales.get(x))
    partidos["acronimo1"] = partidos["equipo 1"].apply(lambda x: acronyms_dict.get(x))
for i in range(len(partidos["equipo 2"])):
    partidos["capitales2"] = partidos["equipo 2"].apply(lambda x: capitales.get(x))
    partidos["acronimo2"] = partidos["equipo 2"].apply(lambda x: acronyms_dict.get(x))



partidos.dropna()



import datetime
#Transform date into format for twitter
for i in range(len(partidos["Date"])):
    partidos["Date"][i]=datetime.datetime.strptime(partidos["Date"][i].replace('_x000D_',''), "%d-%m-%Y").strftime("%Y-%m-%d")




#Create keywords for search
partidos['kw1'] = partidos[['equipo 1', 'equipo 2']].agg(''.join, axis=1)
partidos['kw2'] = partidos[['equipo 1', 'equipo 2']].agg('-'.join, axis=1)
partidos['kw3'] = partidos[['equipo 1', 'equipo 2']].agg('_'.join, axis=1)
partidos['kw4'] = partidos[['equipo 1', 'equipo 2']].agg('vs'.join, axis=1)
partidos['kw4'] = partidos[['equipo 1', 'equipo 2']].agg('vs'.join, axis=1)


#Call function using keywords and date from matches. Load results in new dataframe.

#tweets=pd.DataFrame()
def dates(since): #llamar esta función para cada día
     date_1 = datetime.datetime.strptime(since, '%Y-%m-%d').date()
     dia_1= date_1.strftime('%Y-%m-%d')
     start_date = date_1 - datetime.timedelta(days=1)
     start = start_date.strftime('%Y-%m-%d')
     end_date = date_1 + datetime.timedelta(days=1)
     final = end_date.strftime('%Y-%m-%d')
     fechas=[start,dia_1,final]
     
     return fechas
 
for i in range(len(partidos)):
    
               keywords = [partidos['kw1'][i],partidos['kw2'][i],partidos['kw3'][i],partidos['kw4'][i]]

               fechas=dates(partidos["Date"][i])
               for j in range(len(keywords)):
                   for s in range(len(fechas)):
                       tweets=pd.DataFrame()
                       datos=scrape_tweets(keywords[j],fechas[s],partidos['kw1'][i])
                       tweets=tweets.append(datos,ignore_index=True)
                       time.sleep(100)
                           

               positive = 0
               negative = 0
               neutral = 0
               polarity = 0
               neutral_list = []
               negative_list = []
               positive_list = []
               noOfTweet = len(tweets)
               analyzer = SentimentIntensityAnalyzer()
               
               for tweet in tweets["content"]:
                   analysis = TextBlob(tweet)
                   score = analyzer.polarity_scores(tweet)
                   neg = score['neg']
                   neu = score['neu']
                   pos = score['pos']
                   comp = score['compound']
                   polarity += analysis.sentiment.polarity
               
                   if neg > pos:
                       negative_list.append(tweet)
                       negative += 1
                   elif pos > neg:
                       positive_list.append(tweet)
                       positive += 1
                   elif pos == neg:
                       neutral_list.append(tweet)
                       neutral += 1  
                       


               #
               positive = percentage(positive, noOfTweet)
               negative = percentage(negative, noOfTweet)
               neutral = percentage(neutral, noOfTweet)
               polarity = percentage(polarity, noOfTweet)
               positive = format(positive, '.1f')
               negative = format(negative, '.1f')
               neutral = format(neutral, '.1f')

               #Number of Tweets (Total, Positive, Negative, Neutral)
               tweet_list = pd.DataFrame(tweets["content"])
               neutral_df = pd.DataFrame(neutral_list)
               negative_df = pd.DataFrame(negative_list)
               positive_df = pd.DataFrame(positive_list)
               print('total number: ',len(tweet_list))
               print('positive number: ',len(positive_list))
               print('negative number: ', len(negative_list))
               print('neutral number: ',len(neutral_list))

               #Creating PieChart
               labels = ['Positive ['+str(positive)+'%]' , 'Neutral ['+str(neutral)+'%]','Negative ['+str(negative)+'%]']
               sizes = [positive, neutral, negative]
               colors = ['yellowgreen', 'blue','red']
               patches, texts = plt.pie(sizes,colors=colors, startangle=90)
               plt.style.use('default')
               plt.legend(labels)
               plt.title(f'Sentiment Analysis Result for tweets of final + {match}+{desde}')
               plt.axis('equal')
               plt.show()

               #Sentiment Analysis of clean text
               #1: Drop duplicates
               tweet_list.drop_duplicates(inplace = True)

               #2: Cleaning Text (RT, Punctuation etc)
               tw_list = pd.DataFrame(tweet_list)
               tw_list["text"] = tw_list['content']
               remove_rt = lambda x: re.sub("RT @\w+: "," ",x)
               rt = lambda x: re.sub("(#)|(@[A-Za-z0–9_]+)|(\t)|(\r)|(\n)|(\w+:\/\/\S+)"," ",x)
               tw_list['text'] = tw_list.text.map(remove_rt).map(rt)
               tw_list['text'] = tw_list.text.str.replace('&gt; ','and ')
               # Optional to change tweets to lowercase. SentimentIntensityAnalyzer provides different scores if lower or ALLCAPS cases
               #tw_list['text'] = tw_list.text.str.lower()

               #Calculating Negative, Positive, Neutral and Compound values
               tw_list[['polarity', 'subjectivity']] = tw_list['text'].apply(lambda Text: pd.Series(TextBlob(Text).sentiment))
               for index, row in tw_list['text'].iteritems():
                score = SentimentIntensityAnalyzer().polarity_scores(row)
                neg = score['neg']
                neu = score['neu']
                pos = score['pos']
                comp = score['compound']
                tw_list.loc[index, 'neg'] = neg
                tw_list.loc[index, 'neu'] = neu
                tw_list.loc[index, 'pos'] = pos
                tw_list.loc[index, 'compound'] = comp
                if neg > pos:
                   tw_list.loc[index, 'sentiment'] = 'negative'
                elif pos > neg:
                   tw_list.loc[index, 'sentiment'] = 'positive'
                else:
                    tw_list.loc[index, 'sentiment'] = 'neutral'

               # create data for Pie Chart
               pichart = count_values_in_column(tw_list,'sentiment')
               names = pichart.index
               size = pichart['Percentage']

               # Create a circle for the center of the plot
               my_circle = plt.Circle((0, 0), 0.7, color='white')
               plt.pie(size, labels=names, colors=['green', 'blue', 'red'])
               p = plt.gcf()
               p.gca().add_artist(my_circle)
               plt.style.use('default')
               plt.legend(labels)
               plt.title(f'Sentiment Analysis Result for tweets of Eurocup FInal+ {match}+{desde}')
               plt.axis('equal')
               plt.show()

               #Creating new data frames for all sentiments (positive, negative and neutral)
               tw_list_negative = tw_list[tw_list['sentiment']=='negative']
               tw_list_positive = tw_list[tw_list['sentiment']=='positive']
               tw_list_neutral = tw_list[tw_list['sentiment']=='neutral']

               #Creating clouds of most used words per sentiment
               create_wordcloud(tw_list['text'].values,f"all_sentiments+{match}+{desde}")
               create_wordcloud(tw_list_negative['text'].values,f"negatives+{match}+{desde}")
               create_wordcloud(tw_list_positive['text'].values, f"positive+{match}+{desde}")
               create_wordcloud(tw_list_neutral['text'].values, f'neutral+{match}+{desde}') #añadir fecha

               #Calculating tweet’s lenght and word count
               tw_list['text_len'] = tw_list['text'].astype(str).apply(len)
               tw_list['text_word_count'] = tw_list['text'].apply(lambda x: len(str(x).split()))

               sentiment_file = os.path.join(outputdir,'Sentiment_Analysis_Tweets.csv')
               tw_list.to_csv(sentiment_file, index=False)  
               def remove_url(txt):
                   
                   
                   Replace URLs found in a text string with nothing 
                   (i.e. it will remove the URL from the string).

                   Parametersqaqq2q
                   ----------
                   txt : string
                       A text string that you want to parse and remove urls.

                   Returns
                   -------
                   The same txt string with url's removed.
                   
                   

                   return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split())
               #take the data frame with the tweets and start cleaning the column content 
               #tweets=pd.read_csv("2021-07-07+EnglandDenmark.csv")
               all_tweets_no_urls = [remove_url(tweet) for tweet in tweets["content"]]
               all_tweets_no_urls[:5]
               #split content, obtaining all words
               all_tweets_no_urls[0].split()
               all_tweets_no_urls[0].lower().split()

               words_in_tweet = [tweet.lower().split() for tweet in all_tweets_no_urls]
               words_in_tweet[:2]

               # List of all words across tweets
               all_words_no_urls = list(itertools.chain(*words_in_tweet))

               # Create counter
               counts_no_urls = collections.Counter(all_words_no_urls)
               #most common words in the list
               counts_no_urls.most_common(15)
               #create dataframe
               clean_tweets_no_urls = pd.DataFrame(counts_no_urls.most_common(15),
                                            columns=['words', 'count'])

               clean_tweets_no_urls.head()
               clean_tweets_no_urls
               #make a plot with results
               fig, ax = plt.subplots(figsize=(8, 8))

               # Plot horizontal bar graph
               clean_tweets_no_urls.sort_values(by='count').plot.barh(x='words',
                                     y='count',
                                     ax=ax,
                                     color="purple")

               ax.set_title(f"Common Words Found in Tweets (Including All Words)+{match}+{desde}")

               plt.show()
               #download stopwords
               nltk.download('stopwords')


               stop_words = set(stopwords.words('english'))

               # View a few words from the set
               list(stop_words)[0:10]

               words_in_tweet[0]
               #clean results out of stopwords
               tweets_nsw = [[word for word in tweet_words if not word in stop_words]
                             for tweet_words in words_in_tweet]

               #make list with all words without stop words
               all_words_nsw = list(itertools.chain(*tweets_nsw))

               #counter for this list

               counts_nsw = collections.Counter(all_words_nsw)
               #Dataframe with the 15 most common words
               counts_nsw.most_common(15)
               clean_tweets_nsw = pd.DataFrame(counts_nsw.most_common(15),
                                            columns=['words', 'count'])

               fig, ax = plt.subplots(figsize=(8, 8))

               # Plot horizontal bar graph
               clean_tweets_nsw.sort_values(by='count').plot.barh(x='words',
                                     y='count',
                                     ax=ax,
                                     color="purple")

               ax.set_title(f"Common Words Found in Tweets (Without Stop Words)+{match}+{desde}")

               plt.show()
               #start cleaning words out of collection words that we define. For each match we clean the tweets out of the keywords 
               collection_words = [u"\U0001F600-\U0001F64F" ,'edtech','italyvsengland',"italy","euro2020","rome","euro2020final","coming","england","itscomingrome","ita","going","home","italyengland","la","vs","eurofinal","englandvsitaly","eng",'ItalyvsEngland',"ItalyEngland","englandvsdenmark","englandvdenmark","itscominghome","engden","englanddenmark","den","denmark","inghilterradanimarca"]
               #other_words= keywords

               tweets_nsw_nc = [[w for w in word if not w in collection_words]
                                for word in tweets_nsw]
               #tweets_nsw_no = [[w for w in word if not w in other_words]
               #                 for word in tweets_nsw_nc]



               tweets_nsw_nc[0]

               # Flatten list of words in clean tweets
               all_words_nsw_nc = list(itertools.chain(*tweets_nsw_nc))

               # Create counter of words in clean tweets
               counts_nsw_nc = collections.Counter(all_words_nsw_nc)
               counts_nsw_nc.most_common(15)

               clean_tweets_ncw = pd.DataFrame(counts_nsw_nc.most_common(30),
                                            columns=['words', 'count'])
               clean_tweets_ncw.head()

               fig, ax = plt.subplots(figsize=(8, 8))

               # Plot horizontal bar graph
               clean_tweets_ncw.sort_values(by='count').plot.barh(x='words',
                                     y='count',
                                     ax=ax,
                                     color="purple")

               ax.set_title(f"Common Words Found in Tweets (Without Stop or Collection Words)+{match}+{desde}")

               plt.show()


               #counts frequency of most common words in the polarity lists

               count=0
               list_negatives_frequency=[]
               for i in range (len(negative_list)):
                   for j in range(len(clean_tweets_ncw)):
                       word= negative_list[i].lower().split()
                       for s in range(len(word)):
                           if word[s]==clean_tweets_ncw["words"][j]:
                               count+=1
                               list_negatives_frequency.append(word[s])

               words_list_negative = list_negatives_frequency
               counternegative = Counter(words_list_negative)
               #print(counternegative)  
               dfnegative = pd.DataFrame.from_dict(counternegative, orient='index').reset_index()
               dfnegative.to_csv(f"negative+{match}+{desde}.csv")
               count=0
               i=0
               j=0
               list_neutral_frequency=[]
               for i in range (len(neutral_list)):
                   for j in range(len(clean_tweets_ncw)):
                       word= neutral_list[i].lower().split()
                       for s in range(len(word)):
                           if word[s]==clean_tweets_ncw["words"][j]:
                               count+=1
                               list_neutral_frequency.append(word[s])

               words_list_neutral = list_neutral_frequency
               counterneutral = Counter(list_neutral_frequency)
               #print(counterpositive)  
               dfneutral = pd.DataFrame.from_dict(counterneutral, orient='index').reset_index()
               dfneutral.to_csv(f"neutral+{match}+{desde}.csv")
               count=0
               i=0
               j=0
               list_positives_frequency=[]
               for i in range (len(positive_list)):
                   for j in range(len(clean_tweets_ncw)):
                       word= positive_list[i].lower().split()
                       for s in range(len(word)):
                           if word[s]==clean_tweets_ncw["words"][j]:
                               count+=1
                               list_positives_frequency.append(word[s])

               words_list_positive = list_positives_frequency
               counterpositive= Counter(list_positives_frequency)
               print(counterpositive)  
               dfpositive = pd.DataFrame.from_dict(counterpositive, orient='index').reset_index()
               dfpositive.to_csv(f"positive+{match}+{desde}.csv")   
               
        
    
        
              

        # this script in summary

        #1.downloads the tweets
        #2.counts most common words
        #3.makes word clouds with polarity
        #4.counts most common words in polarity lists
#The dataframe tweets contains all of the information regarding one post. We begin the sentiment analysis and the word frequency 
#analysis

#Word frequency 

def remove_url(txt):
    """
    Replace URLs found in a text string with nothing 
    (i.e. it will remove the URL from the string).

    Parametersqaqq2q
    ----------
    txt : string
        A text string that you want to parse and remove urls.

    Returns
    -------
    The same txt string with url's removed.
    
"""
    return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split())
#take the data frame with the tweets and start cleaning the column content 
#tweets=pd.read_csv("2021-07-07+EnglandDenmark.csv")
all_tweets_no_urls = [remove_url(tweet) for tweet in tweets["content"]]
all_tweets_no_urls[:5]
#split content, obtaining all words
all_tweets_no_urls[0].split()
all_tweets_no_urls[0].lower().split()

words_in_tweet = [tweet.lower().split() for tweet in all_tweets_no_urls]
words_in_tweet[:2]

# List of all words across tweets
all_words_no_urls = list(itertools.chain(*words_in_tweet))

# Create counter
counts_no_urls = collections.Counter(all_words_no_urls)
#most common words in the list
counts_no_urls.most_common(15)
#create dataframe
clean_tweets_no_urls = pd.DataFrame(counts_no_urls.most_common(15),
                             columns=['words', 'count'])

clean_tweets_no_urls.head()
clean_tweets_no_urls
#make a plot with results
fig, ax = plt.subplots(figsize=(8, 8))

# Plot horizontal bar graph
clean_tweets_no_urls.sort_values(by='count').plot.barh(x='words',
                      y='count',
                      ax=ax,
                      color="purple")


ax.set_title("Common Words Found in Tweets (Including All Words)")

plt.show()
#download stopwords
nltk.download('stopwords')


stop_words = set(stopwords.words('english'))

# View a few words from the set
list(stop_words)[0:10]

words_in_tweet[0]
#clean results out of stopwords
tweets_nsw = [[word for word in tweet_words if not word in stop_words]
              for tweet_words in words_in_tweet]

#make list with all words without stop words
all_words_nsw = list(itertools.chain(*tweets_nsw))

#counter for this list

counts_nsw = collections.Counter(all_words_nsw)
#Dataframe with the 15 most common words
counts_nsw.most_common(15)
clean_tweets_nsw = pd.DataFrame(counts_nsw.most_common(15),
                             columns=['words', 'count'])

fig, ax = plt.subplots(figsize=(8, 8))

# Plot horizontal bar graph
clean_tweets_nsw.sort_values(by='count').plot.barh(x='words',
                      y='count',
                      ax=ax,
                      color="purple")

ax.set_title("Common Words Found in Tweets (Without Stop Words)")

plt.show()
#start cleaning words out of collection words that we define. For each match we clean the tweets out of the keywords 
collection_words = [u"\U0001F600-\U0001F64F" ,'edtech','italyvsengland',"italy","euro2020","rome","euro2020final","coming","england","itscomingrome","ita","going","home","italyengland","la","vs","eurofinal","englandvsitaly","eng",'ItalyvsEngland',"ItalyEngland","englandvsdenmark","englandvdenmark","itscominghome","engden","englanddenmark","den","denmark","inghilterradanimarca"]
#other_words= keywords

tweets_nsw_nc = [[w for w in word if not w in collection_words]
                 for word in tweets_nsw]
#tweets_nsw_no = [[w for w in word if not w in other_words]
#                 for word in tweets_nsw_nc]



tweets_nsw_nc[0]

# Flatten list of words in clean tweets
all_words_nsw_nc = list(itertools.chain(*tweets_nsw_nc))

# Create counter of words in clean tweets
counts_nsw_nc = collections.Counter(all_words_nsw_nc)
counts_nsw_nc.most_common(15)

clean_tweets_ncw = pd.DataFrame(counts_nsw_nc.most_common(30),
                             columns=['words', 'count'])
clean_tweets_ncw.head()

fig, ax = plt.subplots(figsize=(8, 8))

# Plot horizontal bar graph
clean_tweets_ncw.sort_values(by='count').plot.barh(x='words',
                      y='count',
                      ax=ax,
                      color="purple")

ax.set_title("Common Words Found in Tweets (Without Stop or Collection Words)")

plt.show()

#begin sentiment analysis
#Initialize descriptive stats for sentiment analysis of raw text
positive = 0
negative = 0
neutral = 0
polarity = 0
neutral_list = []
negative_list = []
positive_list = []
noOfTweet = len(tweets)
analyzer = SentimentIntensityAnalyzer()

for tweet in tweets["content"]:
    print(tweet)
    analysis = TextBlob(tweet)
    score = analyzer.polarity_scores(tweet)
    neg = score['neg']
    neu = score['neu']
    pos = score['pos']
    comp = score['compound']
    polarity += analysis.sentiment.polarity

    if neg > pos:
        negative_list.append(tweet)
        negative += 1
    elif pos > neg:
        positive_list.append(tweet)
        positive += 1
    elif pos == neg:
        neutral_list.append(tweet)
        neutral += 1
        


#
positive = percentage(positive, noOfTweet)
negative = percentage(negative, noOfTweet)
neutral = percentage(neutral, noOfTweet)
polarity = percentage(polarity, noOfTweet)
positive = format(positive, '.1f')
negative = format(negative, '.1f')
neutral = format(neutral, '.1f')

#Number of Tweets (Total, Positive, Negative, Neutral)
tweet_list = pd.DataFrame(tweets["content"])
neutral_df = pd.DataFrame(neutral_list)
negative_df = pd.DataFrame(negative_list)
positive_df = pd.DataFrame(positive_list)
print('total number: ',len(tweet_list))
print('positive number: ',len(positive_list))
print('negative number: ', len(negative_list))
print('neutral number: ',len(neutral_list))

#Creating PieChart
labels = ['Positive ['+str(positive)+'%]' , 'Neutral ['+str(neutral)+'%]','Negative ['+str(negative)+'%]']
sizes = [positive, neutral, negative]
colors = ['yellowgreen', 'blue','red']
patches, texts = plt.pie(sizes,colors=colors, startangle=90)
plt.style.use('default')
plt.legend(labels)
plt.title('Sentiment Analysis Result for tweets of final')
plt.axis('equal')
plt.show()

#Sentiment Analysis of clean text
#1: Drop duplicates
tweet_list.drop_duplicates(inplace = True)

#2: Cleaning Text (RT, Punctuation etc)
tw_list = pd.DataFrame(tweet_list)
tw_list["text"] = tw_list['content']
remove_rt = lambda x: re.sub("RT @\w+: "," ",x)
rt = lambda x: re.sub("(#)|(@[A-Za-z0–9_]+)|(\t)|(\r)|(\n)|(\w+:\/\/\S+)"," ",x)
tw_list['text'] = tw_list.text.map(remove_rt).map(rt)
tw_list['text'] = tw_list.text.str.replace('&gt; ','and ')
# Optional to change tweets to lowercase. SentimentIntensityAnalyzer provides different scores if lower or ALLCAPS cases
#tw_list['text'] = tw_list.text.str.lower()

#Calculating Negative, Positive, Neutral and Compound values
tw_list[['polarity', 'subjectivity']] = tw_list['text'].apply(lambda Text: pd.Series(TextBlob(Text).sentiment))
for index, row in tw_list['text'].iteritems():
 score = SentimentIntensityAnalyzer().polarity_scores(row)
 neg = score['neg']
 neu = score['neu']
 pos = score['pos']
 comp = score['compound']
 tw_list.loc[index, 'neg'] = neg
 tw_list.loc[index, 'neu'] = neu
 tw_list.loc[index, 'pos'] = pos
 tw_list.loc[index, 'compound'] = comp
 if neg > pos:
    tw_list.loc[index, 'sentiment'] = 'negative'
 elif pos > neg:
    tw_list.loc[index, 'sentiment'] = 'positive'
 else:
     tw_list.loc[index, 'sentiment'] = 'neutral'

# create data for Pie Chart
pichart = count_values_in_column(tw_list,'sentiment')
names = pichart.index
size = pichart['Percentage']

# Create a circle for the center of the plot
my_circle = plt.Circle((0, 0), 0.7, color='white')
plt.pie(size, labels=names, colors=['green', 'blue', 'red'])
p = plt.gcf()
p.gca().add_artist(my_circle)
plt.style.use('default')
plt.legend(labels)
plt.title('Sentiment Analysis Result for tweets of Eurocup FInal')
plt.axis('equal')
plt.show()

#Creating new data frames for all sentiments (positive, negative and neutral)
tw_list_negative = tw_list[tw_list['sentiment']=='negative']
tw_list_positive = tw_list[tw_list['sentiment']=='positive']
tw_list_neutral = tw_list[tw_list['sentiment']=='neutral']

#Creating clouds of most used words per sentiment
create_wordcloud(tw_list['text'].values, 'all_sentiments+{EngDen}')
create_wordcloud(tw_list_negative['text'].values, 'negatives+{EngDen}')
create_wordcloud(tw_list_positive['text'].values, "positive+{EngDen}")
create_wordcloud(tw_list_neutral['text'].values, 'neutral+{EngDen}') #añadir fecha

#Calculating tweet’s lenght and word count
tw_list['text_len'] = tw_list['text'].astype(str).apply(len)
tw_list['text_word_count'] = tw_list['text'].apply(lambda x: len(str(x).split()))

sentiment_file = os.path.join(outputdir,'Sentiment_Analysis_Tweets.csv')
tw_list.to_csv(sentiment_file, index=False)


#counts frequency of most common words in the polarity lists

count=0
list_negatives_frequency=[]
for i in range (len(negative_list)):
    for j in range(len(clean_tweets_ncw)):
        word= negative_list[i].lower().split()
        for s in range(len(word)):
            if word[s]==clean_tweets_ncw["words"][j]:
                count+=1
                list_negatives_frequency.append(word[s])

words_list_negative = list_negatives_frequency
counternegative = Counter(words_list_negative)
#print(counternegative)  
dfnegative = pd.DataFrame.from_dict(counternegative, orient='index').reset_index()

count=0
i=0
j=0
list_neutral_frequency=[]
for i in range (len(neutral_list)):
    for j in range(len(clean_tweets_ncw)):
        word= neutral_list[i].lower().split()
        for s in range(len(word)):
            if word[s]==clean_tweets_ncw["words"][j]:
                count+=1
                list_neutral_frequency.append(word[s])

words_list_neutral = list_neutral_frequency
counterneutral = Counter(list_neutral_frequency)
#print(counterpositive)  
dfneutral = pd.DataFrame.from_dict(counterneutral, orient='index').reset_index()

count=0
i=0
j=0
list_positives_frequency=[]
for i in range (len(positive_list)):
    for j in range(len(clean_tweets_ncw)):
        word= positive_list[i].lower().split()
        for s in range(len(word)):
            if word[s]==clean_tweets_ncw["words"][j]:
                count+=1
                list_positives_frequency.append(word[s])

words_list_positive = list_positives_frequency
counterpositive= Counter(list_positives_frequency)
print(counterpositive)  
dfpositive = pd.DataFrame.from_dict(counterpositive, orient='index').reset_index()

# this script in summary

#1.downloads the tweets
#2.counts most common words
#3.makes word clouds with polarity
#4.counts most common words in polarity lists

