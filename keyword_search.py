import tweepy

# Twitter Developer Account Info.
API_KEY = ***REMOVED***
API_SECRET = ***REMOVED***
ACCESS_KEY = ***REMOVED***
ACCESS_SECRET = ***REMOVED***

oAuth = tweepy.OAuthHandler(API_KEY, API_SECRET)
oAuth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth_handler=oAuth)

query = '@Jaemyung_Lee'
max_tweets = 10
i=0
for status in tweepy.Cursor(api.search, q=query).items(max_tweets):
    print(i)
    i+=1
    print(status.id)
    print(status.user.screen_name)
    print(status.text)
    if(status.in_reply_to_status_id == None):
        print("No reply")
    else:
        print(status.in_reply_to_screen_name)
        print(status.in_reply_to_status_id)

