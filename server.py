import wolframalpha as wa
import clientKeys as ck
import serverKeys as api
import socket
import pickle
from cryptography.fernet import Fernet
import hashlib
from subprocess import call
from .serverKeys import *
import sys

# Function takes in plain text and returns plaintext too
def getfromwolfram(question):

	# init the client from wolfram
	client = wa.Client(api.api_wolfram)

	#print the question and receive answer
	print(question)
	result = client.query(question)

	# grab the plaintext answer
	try:
		answer = next(result.results).text
	except StopIteration:
		answer = "No Results"

	# print and return
	print(answer)
	return answer


def text2speech(text):

	cmd_begin = "espeak "
	cmd_end = " 2>/dev/null"

	print(text)

	call([cmd_begin + text + cmd_end], shell=True)


parser = argparse.ArgumentParser(description='Client program of Assignment 1.')
parser.add_argument('-p', type=int, required=True, help='The port number of the connection', dest='port')
parser.add_argument('-z', type=int, required=True, help='The size of the socket', dest='size')
parser.add_argument('-b', type=str, required=True, help='Server backlog', dest='backlog')
arguments = parser.parse_args()

port = arguments.port
size = arguments.size
backlog = arguments.backlog
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("[Checkpoint] Created socket at 0.0.0.0 on port " + port)
s.bind(('',port))
while True:
	s.listen(5)
	print("[Checkpoint] Listening for client connections")
	client, address = s.accept()
	print("[Checkpoint] Accepted client connection from"
		  + address[0] + " on port " + address[1])
	packed_data = client.recv(size)
	data = pickle.loads(packed_data)
	print("[Checkpoint] Received data: " + data[1])
	hasher = hashlib.md5()
	hasher.update(data[1])
	checksum = hasher.hexDigest()
	if checksum == data[2]:
		print("[Checkpoint] Checksum is VALID")
	else:
		print("[Checkpoint] Checksum is NOT VALID")
		continue
	f = Fernet(data[0])
	question = f.decrypt(data[1])
	print("[Checkpoint] Decrypt: Using Key: " + data[0] + " | Plaintext: " + question)
	print("[Checkpoint] Speaking: " + question)
	parsed = question.replace("$", "\$").replace("\"", "\\\"")
	text2speech(question)

