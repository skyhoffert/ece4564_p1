import wolframalpha as wa
import clientKeys as ck
import serverKeys as api
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

