#!/usr/bin/env python3
"""
A simple echo client
"""

import socket
import sys

# declaring variables
host = '0.0.0.0'
port = 0000
size = 1024
tag  = 'Olympics'

# parse arguments
for i in range(1, len(sys.argv)):
    print('arg ', i, ': ', sys.argv[i])
    if '-s' in sys.argv[i]:
        host = sys.argv[i+1]
        i += 1
    if '-p' in sys.argv[i]:
        port = int(sys.argv[i+1])
        i += 1
    if '-z' in sys.argv[i]:
        size = int(sys.argv[i+1])
        i += 1
    if '-t' in sys.argv[i]:
        tag = sys.argv[i+1]
        i += 1

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# set up authentication with clientKeys file
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
# connect to the API
api = tweepy.API(auth)

# create listener
l = MyStreamListener()
mystream = tweepy.Stream(auth = api.auth, listener = l)
# tell the listener to track the indicated search string
# add 'async=True' for non-blocking call
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
        
        print('Connecting to host at ', host, ' on port ', port)
        s.connect((host,port))

        print('Sending question to server')
        s.send(res)

        print('Receiving data with size ', size)

        data = s.recv(size)
        s.close()
        print('Received:', data)
