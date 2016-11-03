# My ID : 553557460
import tweepy
import mysql.connector as msc
import pandas as pd

API_KEY = ***REMOVED***
API_SECRET = ***REMOVED***
ACCESS_KEY = ***REMOVED***
ACCESS_SECRET = ***REMOVED***

oAuth = tweepy.OAuthHandler(API_KEY, API_SECRET)
oAuth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth_handler=oAuth)

if __name__ == '__main__':
    userID = '881373588'
    user = api.get_user(user_id=userID)
    timeline = api.user_timeline(user_id=userID, count=205)

    # Print User's Timeline Tweets
    i=0
    for tweet in timeline:
        try:
            texts = tweet.text
            
            #print(i)
            #i+=1
            #print("Tweet: ", texts)
            
            #print(type(texts))

        except AttributeError as e:
            print("ERROR: ", e)


    for status in tweepy.Cursor(api.user_timeline, user_id=userID).items():
        print(i)
        i+=1
        # created_at: 표준시로 나옴
        print(status.created_at)
        print(status.text)


