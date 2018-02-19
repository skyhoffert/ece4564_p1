#!/usr/bin/env python3
"""
A simple echo client
"""

import socket
import sys
import argparse
import os
import tweepy
import hashlib
import pickle
from cryptography.fernet import Fernet
from clientKeys import *

#PARSE THEM ARGS MATEY!

parser = argparse.ArgumentParser(description='Client program of Assignment 1.')
parser.add_argument('-s', type=str, required=True, help='The ip address of the server', dest='host')
parser.add_argument('-p', type=int, required=True, help='The port number of the connection', dest='port')
parser.add_argument('-z', type=int, required=True, help='The size of the socket', dest='size')
parser.add_argument('-t', type=str, required=True, help='Hashtag to be watched', dest='hashtag')
arguments = parser.parse_args()

#print(arguments.host)
#print(arguments.port)
#print(arguments.size)
#print(arguments.hashtag)


# declaring variables IGNORED
host = arguments.host
port = arguments.port
size = arguments.size
tag  = arguments.hashtag

# set up authentication with clientKeys file
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
# connect to the API
api = tweepy.API(auth)

# Tweepy stream listener class
class MyStreamListener(tweepy.StreamListener):
    # whenever a new post is made with the search string, this function is called
    # on_status means the filter found a status update, or tweet
    def on_status(self, status):
        # get the string result
        res = status.text
        # Cut out the substring so we have just a raw question
        res = res.replace(tag, '')

        key = Fernet.generate_key()

        print('Creating crypto key: ', key)
        f = Fernet(key)

        # encrypt
        # convert text question to bytes object
        text = bytes(res, 'utf-8')
        print('text to be sent: ', text)
        token = f.encrypt(text)

        print('token: ', token)

        # hash
        hasher = hashlib.md5()
        hasher.update(token)
        checksum = hasher.hexdigest()

        print('checksum: ', checksum)

        # channel
        val = (key, token, checksum)

        val = pickle.dumps(val)

        print('Val to be sent over channel: ', val)

        print('Creating socket object')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print('Connecting to host at ', host, ' on port ', port)
        s.connect((host,port))

        print('Sending question to server')
        s.send(val)

        print('Receiving data with size ', size)
        data = s.recv(size)
        s.close()
        del s
        print('Raw received: ', data)

        package = pickle.loads(data)

        rx_hasher = hashlib.md5()
        rx_hasher.update(package[0])
        rx_checksum = rx_hasher.hexdigest()

        print('package[1]: ', package[1])
        print('Checksum: ', rx_checksum)
        if rx_checksum == package[1]:
            print('Checksum was correct')
        else:
            print('Invalid checksum')

        answer = f.decrypt(package[0])

        print('Speaking answer: ', answer)
        print('Str answer: ', answer.decode('utf-8'))
        os.system("espeak \"{}\" 2>/dev/null".format(answer.decode('utf-8')))

# create listener
l = MyStreamListener()
mystream = tweepy.Stream(auth = api.auth, listener = l)
# tell the listener to track the indicated search string
# add 'async=True' for non-blocking call
mystream.filter(track=[tag])
