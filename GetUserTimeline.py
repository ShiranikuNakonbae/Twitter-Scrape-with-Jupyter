# Python Script to Extract user tweets of a
# using Tweepy and Pandas
# modifictaion with timezone to covert tweet_created_at
# and export the result to csv


# import modules
import pandas as pd
import tweepy
import os
import pytz
from datetime import datetime

utc_time = datetime.utcnow()
tz = pytz.timezone('Asia/Jakarta')
utc_time = utc_time.replace(tzinfo = pytz.UTC)


# function to display data of each tweet
def printtweetdata(n, ith_tweet):
	print()
	print(f"Tweet {n}:")
	print(f"Username:{ith_tweet[0]}")
	print(f"Description:{ith_tweet[1]}")
	print(f"Location:{ith_tweet[2]}")
	print(f"Following Count:{ith_tweet[3]}")
	print(f"Follower Count:{ith_tweet[4]}")
	print(f"Tweets Count:{ith_tweet[5]}")
	print(f"Is Verified:{ith_tweet[6]}")
	print(f"Tweet Created At:{ith_tweet[7]}")
	print(f"Tweet Text:{ith_tweet[8]}")
	print(f"Retweet Count:{ith_tweet[9]}")
	print(f"Favorite Count:{ith_tweet[10]}")
	print(f"In Reply To:{ith_tweet[11]}")
	print(f"Source:{ith_tweet[12]}")
	print(f"Hashtags Used:{ith_tweet[13]}")


# function to perform data extraction
def scrape(username, count):
	
	# Creating DataFrame using pandas
	db = pd.DataFrame(columns=['username', 'description', 'location', 'followingcount',
			'followerscount', 'tweetscount','IsVerified', 'TweetCreatedAt', 'text', 'retweetcount', 'favoritecount', 'InReplyTo', 'source', 'hashtags'])
	   
	# We are using .Cursor() to search through twitter for the required tweets.
	# The number of tweets can be restricted using .items(number of tweets)
	tweets = tweepy.Cursor(api.user_timeline, screen_name=username, tweet_mode='extended').items(count)
	
	# .Cursor() returns an iterable object. Each item in
	# the iterator has various attributes that you can access to
	# get information about each tweet
	list_tweets = [tweet for tweet in tweets]
	
	# Counter to maintain Tweet Count
	i = 1
	
	# we will iterate over each tweet in the list for extracting information about each tweet
	for tweet in list_tweets:
		username = tweet.user.screen_name
		description = tweet.user.description
		location = tweet.user.location
		followingcount = tweet.user.friends_count
		followerscount = tweet.user.followers_count
		newtweet = tweet._json['full_text']       
		tweetscount = tweet.user.statuses_count
		IsVerified = tweet.user.verified
		TweetCreatedAt = (tweet.created_at).astimezone(tz)
		retweetcount = tweet.retweet_count
		favoritecount = tweet.favorite_count
		InReplyTo = tweet.in_reply_to_screen_name
		source = tweet.source
		hashtags = tweet.entities['hashtags']
		
    
		hashtext = list()
		for j in range(0, len(hashtags)):
			hashtext.append(hashtags[j]['text'])
		
		# Here we are appending all the extracted information in the DataFrame
		ith_tweet = [username, description, location, followingcount,
					followerscount, tweetscount, IsVerified, TweetCreatedAt, newtweet, retweetcount, favoritecount, InReplyTo, source, hashtext]
		db.loc[len(db)] = ith_tweet
		
		# Function call to print tweet data on screen
		printtweetdata(i, ith_tweet)
		i = i+1
	filename = os.path.join(fname)
	
	# we will save our database as a CSV file.
	db.to_csv(filename)


if __name__ == '__main__':
	
	# Enter your own credentials obtained
	# from your developer account
	consumer_key = "dY1AWrR2dDySXkl7me5BV0P9w"
	consumer_secret = "lLrbr7oXMZyONTyR38JLLqvit7Sl063pgXw9ZyiPcauf1AsX9N"
	access_key = "219652337-HhGfeiELGVbRkjAHIopYF0Hu7aCdhCdX6HQ7h8EX"
	access_secret = "VBNe637tOPUX5wbL2lW6cGpYhZcK9PG1FCzcNv4uXOMiZ"
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	
	# Enter Hashtag and initial date
	print("Enter Timeline's Username")
	username = input()
	print("Name a File")
	fname = input() + '.csv'
	print("Enter Number of Tweet")
	count = int(input())

	
	# number of tweets you want to extract in one run
	scrape(username, count)
	print('Scraping has completed!')
