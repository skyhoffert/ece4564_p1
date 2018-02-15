# Sky Hoffert
# test_stream_listen_tweepy.py
# Febrary 13, 2018
# p1
# Team 02

import tweepy

from clientKeys import *

search_str='#ECE4564T02'
#search_str='Olympics'

def main():
    # set up authentication with clientKeys file
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    # connect to the API
    api = tweepy.API(auth)

    # create listener
    l = MyStreamListener()
    mystream = tweepy.Stream(auth = api.auth, listener = l)
    # tell the listener to track the indicated search string
    mystream.filter(track=[search_str])

# Tweepy stream listener class
class MyStreamListener(tweepy.StreamListener):

    # whenever a new post is made with the search string, this function is called
    # on_status means the filter found a status update, or tweet
    def on_status(self, status):
        # get the string result
        res = status.text
        # Cut out the substring so we have just a raw question
        res = res.replace(search_str, '')

        # DEBUG
        print('modified:', res)

if __name__ == '__main__':
    main()
