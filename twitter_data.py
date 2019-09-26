# Author:  Sanchita Rastogi
# ID: 10439951
# Subject: Online Social Networks

# twitter_data.py searches Twitter for tweets matching a search term,
#      up to a maximun number

######  user must supply authentication keys where indicated

# to run from terminal window: 
#        python3  twitter_data.py   --search_term1  mysearch1 --search_term2  mysearch2  --search_max  mymaxresults 
# where:  mysearch is the term the user wants to search for;  default = music and photo
#   and:  mymaxresults is the maximum number of results;  default = 30

#   I used --search_term as "music" and search_max = 30
#   I am calculating the Mininmum and Maximum values for retweets, followers, friends column
#   and also calculating the sum of the whole column

# other options used in the search:  lang = "en"  (English language tweets)
#  and  result_type = "popular"  (asks for most popular rather than most recent tweets)

# The program uses the TextBlob sentiment property to analyze the tweet for:
#  polarity (range -1 to 1)  and  
#  subjectivity (range 0 to 1 where 0 is objective and 1 is subjective)

# The program creates a .csv output file with a line for each tweet
#    including tweet data items and the sentiment information

from textblob import TextBlob	# needed to analyze text for sentiment
import argparse    				# for parsing the arguments in the command line
import csv						# for creating output .csv file
import tweepy					# Python twitter API package
import unidecode				# for processing text fields in the search results
import pandas as pd         # need for read, manipulation and analysis 
import numpy as np          # need for mathematical function

### PUT AUTHENTICATOIN KEYS HERE ###
CONSUMER_KEY = ""
CONSUMER_KEY_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""

# AUTHENTICATION (OAuth)
authenticate = tweepy.auth.OAuthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)
authenticate.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(authenticate)

# Get the input arguments - search_term and search_max
parser = argparse.ArgumentParser(description='Twitter Search')
parser.add_argument("--search_term1", action='store', dest='search_term1', default="music")
parser.add_argument("--search_term2", action='store', dest='search_term2', default="photo")
parser.add_argument("--search_max", action='store', dest='search_max', default=30)
args = parser.parse_args()

search_term1 = args.search_term1
search_term2 = args.search_term2
search_max = int(args.search_max)

search_terms=[]
search_terms.append(search_term1)
search_terms.append(search_term2)
for search_term in search_terms:
# create a .csv file to hold the results, and write the header line
        csvFile = open('twitter_results_' + search_term + '.csv','w')
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(["username","userid","created", "text", "retweets", "followers",
    "friends","polarity","subjectivity"])

# do the twitter search
        for tweet in tweepy.Cursor(api.search, q = search_term, lang = "en", 
		result_type = "popular").items(search_max):
		
            created = tweet.created_at				# date created
            text = tweet.text						# text of the tweet
            text = unidecode.unidecode(text) 
            retweets = tweet.retweet_count			# number of retweets
            username  = tweet.user.name            	# user name
            userid  = tweet.user.id              	# userid
            followers = tweet.user.followers_count 	# number of user followers
            friends = tweet.user.friends_count      # number of user friends
    
	# use TextBlob to determine polarity and subjectivity of tweet
            text_blob = TextBlob(text)
            polarity = text_blob.polarity
            subjectivity = text_blob.subjectivity
    
	# write tweet info to .csv tile
            csvWriter.writerow([username, userid, created, text, retweets, followers, 
                                friends, polarity, subjectivity])
csvFile.close()
#   reading the csv file using pandas and store it in data
data_1 = pd.read_csv("twitter_results_"+search_terms[0]+".csv")
# MAX and MIN Value in the retweets COLUMN
# MAX and MIN Value in the retweets COLUMN
Max_retweets = (np.where(data_1["retweets"] == np.max(data_1["retweets"])))
print("Max retweets for the tweets Username", data_1.iloc[Max_retweets[0],:].username)
print("Max retweets for the tweets", data_1.iloc[Max_retweets[0],:].retweets)

Min_retweets = (np.where(data_1["retweets"] == np.min(data_1["retweets"])))
print("Min retweets for the tweets Username", data_1.iloc[Min_retweets[0],:].username)
print("Min retweets for the tweets", data_1.iloc[Min_retweets[0],:].retweets)

# MAX and MIN Value in the followers COLUMN
Max_followers = (np.where(data_1["followers"] == np.max(data_1["followers"])))
print("Max followers for the tweets Username", data_1.iloc[Max_followers[0],:].username)
print("Max followers for the tweets", data_1.iloc[Max_followers[0],:].followers)

Min_followers = (np.where(data_1["followers"] == np.min(data_1["followers"])))
print("Min followers for the tweets Username", data_1.iloc[Min_followers[0],:].username)
print("Min followers for the tweets", data_1.iloc[Min_followers[0],:].followers)

# MAX and MIN Value in the friends COLUMN
Max_friends = (np.where(data_1["friends"] == np.max(data_1["friends"])))
print("Max friends for the tweets Username", data_1.iloc[Max_friends[0],:].username)
print("Max friends for the tweets", data_1.iloc[Max_friends[0],:].friends)

Min_friends = (np.where(data_1["friends"] == np.min(data_1["friends"])))
print("Min friends for the tweets Username", data_1.iloc[Min_friends[0],:].username)
print("Min friends for the tweets", data_1.iloc[Min_friends[0],:].friends)

# Polarity as positive, negative and neutral with their count
positive_polarity = 0
neutral_polarity = 0
negative_polarity = 0
for rows in data_1["polarity"]:
    positive_polarity += 1 if rows > 0 else 0
    neutral_polarity += 1 if rows == 0 else 0
    negative_polarity += 1 if rows < 0 else 0

print ("Positive Tweets counts:", positive_polarity)
print ("Neutral Tweets counts:", neutral_polarity)
print ("Negative Tweets counts:", negative_polarity)
    
# Analysis on second search
#   reading the csv file using pandas and store it in data
data_2 = pd.read_csv("twitter_results_"+search_terms[1]+".csv")
# MAX and MIN Value in the retweets COLUMN
Max_retweets = (np.where(data_2["retweets"] == np.max(data_2["retweets"])))
print("Max retweets for the tweets Username", data_2.iloc[Max_retweets[0],:].username)
print("Max retweets for the tweets", data_2.iloc[Max_retweets[0],:].retweets)

Min_retweets = (np.where(data_2["retweets"] == np.min(data_2["retweets"])))
print("Min retweets for the tweets Username", data_2.iloc[Min_retweets[0],:].username)
print("Min retweets for the tweets", data_2.iloc[Min_retweets[0],:].retweets)

# MAX and MIN Value in the followers COLUMN
Max_followers = (np.where(data_2["followers"] == np.max(data_2["followers"])))
print("Max followers for the tweets Username", data_2.iloc[Max_followers[0],:].username)
print("Max followers for the tweets", data_2.iloc[Max_followers[0],:].followers)

Min_followers = (np.where(data_2["followers"] == np.min(data_2["followers"])))
print("Min followers for the tweets Username", data_2.iloc[Min_followers[0],:].username)
print("Min followers for the tweets", data_2.iloc[Min_followers[0],:].followers)

# MAX and MIN Value in the friends COLUMN
Max_friends = (np.where(data_2["friends"] == np.max(data_2["friends"])))
print("Max friends for the tweets Username", data_2.iloc[Max_friends[0],:].username)
print("Max friends for the tweets", data_2.iloc[Max_friends[0],:].friends)

Min_friends = (np.where(data_2["friends"] == np.min(data_2["friends"])))
print("Min friends for the tweets Username", data_2.iloc[Min_friends[0],:].username)
print("Min friends for the tweets", data_2.iloc[Min_friends[0],:].friends)

# Polarity as positive, negative and neutral with their count
positive_polarity = 0
neutral_polarity = 0
negative_polarity = 0
for rows in data_2["polarity"]:
    positive_polarity += 1 if rows > 0 else 0
    neutral_polarity += 1 if rows == 0 else 0
    negative_polarity += 1 if rows < 0 else 0

print ("Positive Tweets counts:", positive_polarity)
print ("Neutral Tweets counts:", neutral_polarity)
print ("Negative Tweets counts:", negative_polarity)

    


















