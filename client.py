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

print('Connecting to host at ', host, ' on port ', port)

s.connect((host,port))
s.send(b'Hello, world')

print('Receiving data with size ', size)

data = s.recv(size)
s.close()
print ('Received:', data)
