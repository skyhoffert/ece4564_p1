#!/usr/bin/env python3
"""
A simple echo client
"""

import socket
import sys
import argparse

#PARSE THEM ARGS MATEY!

parser = argparse.ArgumentParser(description='Client program of Assignment 1.')
parser.add_argument('-s', type=str, required=True, help='The ip address of the server', dest='host')
parser.add_argument('-p', type=int, required=True, help='The port number of the connection', dest='port')
parser.add_argument('-z', type=int, required=True, help='The size of the socket', dest='size')
parser.add_argument('-t', type=str, required=True, help='Hashtag to be watched', dest='hashtag')
arguments = parser.parse_args()

print(arguments.host)
print(arguments.port)
print(arguments.size)
print(arguments.hashtag)

# declaring variables IGNORED
host = arguments.host
port = arguments.port
size = arguments.size
tag  = arguments.hashtag

# parse arguments
#for i in range(1, len(sys.argv)):
#    print('arg ', i, ': ', sys.argv[i])
#    if '-s' in sys.argv[i]:
#        host = sys.argv[i+1]
#        i += 1
#    if '-p' in sys.argv[i]:
#        port = int(sys.argv[i+1])
#        i += 1
#    if '-z' in sys.argv[i]:
#        size = int(sys.argv[i+1])
#        i += 1
#    if '-t' in sys.argv[i]:
#        tag = sys.argv[i+1]
#        i += 1

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print('Connecting to host at ', host, ' on port ', port)

s.connect((host,port))
s.send(b'Hello, world')

print('Receiving data with size ', size)

data = s.recv(size)
s.close()
print ('Received:', data)
