import wolframalpha as wa
import serverKeys as api
import socket
import pickle
from cryptography.fernet import Fernet
import hashlib
from subprocess import call
import argparse

# Function takes in plain text and returns plaintext too
def getfromwolfram(question):

	# init the client from wolfram
	client = wa.Client(api.api_wolfram)

	#print the question and receive answer
	result = client.query(question)

	# grab the plaintext answer
	try:
		answer = next(result.results).text
	except:
		answer = "No Results"

	# print and return
	return answer


def text2speech(text):

	cmd_begin = "espeak "
	cmd_end = " 2>/dev/null"


	call([cmd_begin + text + cmd_end], shell=True)


parser = argparse.ArgumentParser(description='Client program of Assignment 1.')
parser.add_argument('-p', type=int, required=True, help='The port number of the connection', dest='port')
parser.add_argument('-z', type=int, required=True, help='The size of the socket', dest='size')
parser.add_argument('-b', type=int, required=True, help='Server backlog', dest='backlog')
arguments = parser.parse_args()

port = arguments.port
size = arguments.size
backlog = arguments.backlog
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("[Checkpoint] Created socket at 0.0.0.0 on port", port)
s.bind(('', port))
s.listen()
print("[Checkpoint] Listening for client connections")
while True:
	client, address = s.accept()
	print("[Checkpoint] Accepted client connection from",
		  address[0], " on port", address[1])
	packed_data = client.recv(size)
	data = pickle.loads(packed_data)
	print("[Checkpoint] Received data:", data[1])
	hasher = hashlib.md5()
	hasher.update(data[1])
	checksum = hasher.hexdigest()
	if checksum == data[2]:
		print("[Checkpoint] Checksum is VALID")
	else:
		print("[Checkpoint] Checksum is NOT VALID")
		continue
	f = Fernet(data[0])
	question = f.decrypt(data[1]).decode('utf-8')
	print("[Checkpoint] Decrypt: Using Key:", data[0], " | Plaintext:", question)
	print("[Checkpoint] Speaking:" + question)
	parsed = question.replace("$", "\$").replace("\"", "\\\"")
	text2speech("\"" + parsed + "\"")
	print("[Checkpoint] Sending question to Wolframalpha:", question)
	answer = getfromwolfram(question)
	print("[Checkpoint] Received answer from Wolframalpha:", answer)
	answer = f.encrypt(answer.encode('utf-8'))
	print("[Checkpoint] Encrypt: Generated Key:", data[0],
		  " | Ciphertext: ", answer)
	hasher = hashlib.md5()
	hasher.update(answer)
	checksum = hasher.hexdigest()
	print("[Checkpoint] Generated MD5 Checksum:", checksum)
	payload = (answer, checksum)
	payload = pickle.dumps(payload)
	print("[Checkpoint] Sending data:", payload)
	client.send(payload)
	client.close()
