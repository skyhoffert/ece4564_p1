# Sky Hoffert
# April 27, 2018
# simulate.py
# Project 4 for ECE 2500

# NOTES:
# Must be run with python 2.7

import sys

# util functions ---------------------------------------------------------------------------------------------------------------
def print_smart( val, debug=False, error=False, end='\n', prefix=True ):
	# modify string to fit given args
	val = str( val )
	val = '[ ERROR ] ' + val if error else '[ DEBUG ] ' + val if debug else '[ PROGR ] ' + val if prefix else val
	val = val + end if end else val
	
	# print and flush
	sys.stdout.write( val )
	sys.stdout.flush()

# classes ----------------------------------------------------------------------------------------------------------------------
class Cache():
	'''Class to hold a variety of different cache designs'''

	def __init__(self, size=0, block_size=0, placement='', policy=''):
		self._size = size             # size of the cache, in bytes
		self._block_size = block_size # size of a block, in bytes
		self._placement = placement   # type of mapping as a string
		self._policy = policy         # type of write policy as a string
	
	def read(self, addr):
		return
	
	def write(self, addr):
		return
	
	def get_hit_rate(self):
		return
	
	def get_mem_to_cache(self):
		return
	
	def get_cache_to_mem(self):
		return
	
# main program -----------------------------------------------------------------------------------------------------------------
def main():
	input_filename  = 'test.trace'
	output_filename = 'test.result'
	
	# handle arguments
	if len( sys.argv ) is 1:
		pass
	elif len( sys.argv ) is 2:
		input_filename = str( sys.argv[1] )
	elif len( sys.argv ) is 3:
		input_filename  = str( sys.argv[1] )
		output_filename = str( sys.argv[2] )
	else:
		print_smart( 'Invalid number of input arguments. Exiting...', error=True )
		sys.exit( 1 )
		
	# create all the different caches
	caches = []
	for size in [1024, 4096, 65536, 131072]:
		for block_size in [8, 16, 32, 128]:
			for placement in ['DM', '2W', '4W', 'FA']:
				for policy in ['WB', 'WT']:
					caches.append( Cache(size=size, block_size=block_size, placement=placement, policy=policy) )
	
	# open the input file
	try:
		f_in  = open( input_filename,  'r' )
	except:
		print_smart( 'Could not open given input filename: "{}". Exiting...'.format(input_filename), error=True )
		sys.exit( 1 )
	
	print_smart( 'Opening input file.' )
	
	# iterate through input file
	for line in f_in.readlines():
		tokenized = line.rstrip().split(' ')
		if tokenized[0] == 'read':
			pass
		elif tokenized[0] == 'write':
			pass
	
	# don't forget to close input file!
	f_in.close()
	
	# open the output file
	f_out = open( output_filename, 'w' )
	
	# TODO
	
	f_out.close()

# this is called on execution --------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	main()
	sys.exit()