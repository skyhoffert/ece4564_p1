# from num2words import num2words
from subprocess import call


def text2speech(text):

	cmd_begin = "espeak "
	cmd_end = " 2>/dev/null"

	print(text)

	call([cmd_begin + text + cmd_end], shell=True)
