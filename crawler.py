# My ID : 553557460
# Ahn-cheolsoo0919 : 881373588
# Moon-moonriver365 : 444465942
# Kim-kimmoosung : 50879035


import tweepy

Joohong = '553557460'
Ahn = '881373588'
Moon = '444465942'
Kim = '50879035'

API_KEY = ***REMOVED***
API_SECRET = ***REMOVED***
ACCESS_KEY = ***REMOVED***
ACCESS_SECRET = ***REMOVED***

oAuth = tweepy.OAuthHandler(API_KEY, API_SECRET)
oAuth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth_handler=oAuth)

if __name__ == '__main__':
    userID = Ahn
    user = api.get_user(user_id=userID)
    timeline = api.user_timeline(user_id=userID, count=10)

    # Print User's Timeline Tweets
    for tweet in timeline:
        try:
            texts = tweet.text
            print("Tweet: ", texts)
        except AttributeError as e:
            print("ERROR: ", e)
