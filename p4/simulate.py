# Sky Hoffert
# April 27, 2018
# simulate.py
# Project 4 for ECE 2500

# NOTES:
# Must be run with python 2.7

import sys
import math

# util functions ---------------------------------------------------------------------------------------------------------------
def print_smart( val, debug=False, error=False, end='\n', prefix=True ):
    # modify string to fit given args
    val = str( val )
    val = '[ ERROR ] ' + val if error else '[ DEBUG ] ' + val if debug else '[ PROGR ] ' + val if prefix else val
    val = val + end if end else val
    
    # print and flush
    sys.stdout.write( val )
    sys.stdout.flush()

# converts a hex string to an integer
def hexstr_to_int( val ):
    return int( val, 0 )
    

# classes ----------------------------------------------------------------------------------------------------------------------
class Cache():
    '''Class to hold a variety of different cache designs'''

    def __init__(self, size=0, block_size=0, placement='', policy=''):
        self._size = size             # size of the cache, in bytes
        self._block_size = block_size # size of a block, in bytes
        self._placement = placement   # type of mapping as a string
        self._policy = policy         # type of write policy as a string
        
        # calculate bits for each address part
        self._bits_offset = int( math.log( self._block_size, 2 ) )
        
        num_ways = 0
        if self._placement == 'DM':
            self._bits_index  = int( math.log( self._size / self._block_size, 2 ) )
            num_ways = 1
        elif self._placement == '2W':
            self._bits_index  = int( math.log( self._size / (2 * self._block_size), 2 ) )
            num_ways = 2
        elif self._placement == '4W':
            self._bits_index  = int( math.log( self._size / (4 * self._block_size), 2 ) )
            num_ways = 4
        elif self._placement == 'FA':
            self._bits_index = 0
            num_ways = int( self._size / self._block_size )
            
        self._bits_tag    = 32 - self._bits_offset - self._bits_index
        
        # statistic variables
        self._hits   = 0
        self._misses = 0
        self._mem_to_cache = 0
        self._cache_to_mem = 0
        
        # the way to store tags and valid bits, a list of dicts
        self._cache = []
        
        # for fully associative, there is only one cache "set"
        if self._bits_index is 0:
            self._cache.append( { 'lru': 0, 'ways': [] } )
            for j in range(0, num_ways):
                    self._cache[0]['ways'].append( { 'valid_bit': 0, 'dirty_bit': 0, 'tag': 0 } )
        else:
            # other mappings have many sets
            for i in range(0, pow(2, self._bits_index)):
                self._cache.append( { 'lru': 0, 'ways': [] } )
                for j in range(0, num_ways):
                    self._cache[i]['ways'].append( { 'valid_bit': 0, 'dirty_bit': 0, 'tag': 0 } )

    # splits an integer into the correct bits
    # returns tuple ( <offset>, <set>, <tag> )
    def split_to_vals(self, val):
        mask = 0xFFFFFFFF
        off = int(val &  (mask >> (32-self._bits_offset)))
        tag = int(val &  (mask << (32-self._bits_tag))) >> (32-self._bits_tag)
        set = int(val & ((mask >> (32-self._bits_index) << self._bits_offset))) >> self._bits_offset
        
        return ( off, set, tag )
    
    def read(self, addr):
        # get the values from this address
        res = self.split_to_vals( addr )
        
        print_smart( 'Reading', debug=True )
        print_smart( 'Accessing cache line {}'.format( res[1] ), debug=True )
        print_smart( 'Looks like: {}'.format( self._cache[res[1]]['ways'][self._cache[res[1]]['lru']] ), debug=True )
        print_smart( 'For lru: {}'.format( self._cache[res[1]]['lru'] ), debug=True )
        
        # check all possible ways
        way = None
        way_num = -1
        for i, w in enumerate( self._cache[res[1]]['ways'] ):
            if w['tag'] == res[2]:
                if w['valid_bit']:
                    way = w
                    way_num = i
                    self._hits += 1
                    break
                   
        # if there was no way, miss
        if way is None:
            self._misses += 1
                
            # on miss, update tag and valid bit at lru
            self._cache[res[1]]['ways'][self._cache[res[1]]['lru']]['valid_bit'] = 1
            self._cache[res[1]]['ways'][self._cache[res[1]]['lru']]['tag'] = res[2]
            
            # on miss, update lru
            lru = self._cache[res[1]]['lru']
            if lru+1 >= len( self._cache[res[1]]['ways'] ):
                lru = 0
            else:
                lru += 1
            self._cache[res[1]]['lru'] = lru
            
            # if missed, read from memory
            # TODO -- make sure this is correct
            self._mem_to_cache += self._block_size
        else:
            # on hit, check if update to lru is necessary
            if self._cache[res[1]]['lru'] == i:
                lru = i
                if lru+1 >= len( self._cache[res[1]]['ways'] ):
                    lru = 0
                else:
                    lru += 1
                self._cache[res[1]]['lru'] = lru
        
        # still not sure about memory stuff here?
        # TODO -- memory
    
        return
    
    def write(self, addr):
        # get the values from this address
        res = self.split_to_vals( addr )
        
        print_smart( 'Writing', debug=True )
        print_smart( 'Accessing cache line {}'.format( res[1] ), debug=True )
        print_smart( 'Looks like: {}'.format( self._cache[res[1]]['ways'][self._cache[res[1]]['lru']] ), debug=True )
        
        # check the valid bit
        # TODO -- figure out some stuff for writing
        # TODO -- write from mem to cache on write miss
        # TODO -- write to mem when block is dirty
        if not self._cache[res[1]]['ways'][self._cache[res[1]]['lru']]['valid_bit']:
            self._misses += 1
            self._cache[res[1]]['ways'][self._cache[res[1]]['lru']]['valid_bit'] = 1
            self._cache[res[1]]['ways'][self._cache[res[1]]['lru']]['tag'] = res[2]
        else:
            # check the tag
            if self._cache[res[1]]['ways'][self._cache[res[1]]['lru']]['tag'] != res[2]:
                self._misses += 1
            else:
                # tag and valid bit are good, we hit
                self._hits += 1
        
        # memory stuff
        if self._policy == 'WT':
            # always write to mem for write-through
            self._cache_to_mem += self._block_size
        
        return
    
    def get_hit_rate(self):
        return float( float(self._hits) / float( self._hits + self._misses ) )
    
    def get_mem_to_cache(self):
        return self._mem_to_cache
    
    def get_cache_to_mem(self):
        return self._cache_to_mem
    
    def __str__(self):
        val =       'Cache size:  {}\n'.format( self._size )
        val = val + 'Block size:  {}\n'.format( self._block_size )
        val = val + 'Placement:   {}\n'.format( self._placement )
        val = val + 'Policy:      {}\n'.format( self._policy )
        val = val + 'Offset bits: {}\n'.format( self._bits_offset )
        val = val + 'Index bits:  {}\n'.format( self._bits_index )
        val = val + 'Tag bits:    {}\n'.format( self._bits_tag )
        val = val + 'Num Hits:    {}\n'.format( self._hits )
        val = val + 'Num Misses:  {}\n'.format( self._misses )
        val = val + 'CacheToMem:  {}\n'.format( self._cache_to_mem )
        val = val + 'MemToCache:  {}\n'.format( self._mem_to_cache )
        val = val + 'Cache at 0:  {}'.format( self._cache[0] )
        return val
    
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
    
    print_smart( 'Opening input file.' )
    
    # open the input file
    try:
        f_in  = open( input_filename,  'r' )
    except:
        print_smart( 'Could not open given input filename: "{}". Exiting...'.format(input_filename), error=True )
        sys.exit( 1 )
    
    # iterate through input file, reading and writing
    for line in f_in.readlines():
        tokenized = line.rstrip().split(' ')
        if tokenized[0] == 'read':
            for cache in caches:
                cache.read( hexstr_to_int(tokenized[1]) )
        elif tokenized[0] == 'write':
            for cache in caches:
                cache.write( hexstr_to_int(tokenized[1]) )
    
    # DEBUG
    cache_num = 0
    print_smart( 'Results: ============================================================================', debug=True )
    print_smart( 'Hit rate for cache {}: {}'.format(cache_num, caches[cache_num].get_hit_rate()), debug=True )
    print_smart( 'Cache {}:\n{}'.format(cache_num, caches[cache_num]), debug=True )
    
    # don't forget to close input file!
    f_in.close()
    
    # open the output file
    f_out = open( output_filename, 'w' )
    
    for cache in caches:
        f_out.write( '{} {} {} {} {} {} {}\n'.format(cache._size, cache._block_size, cache._placement, cache._policy, cache.get_hit_rate(), cache.get_mem_to_cache(), cache.get_cache_to_mem()) )
    
    # close output file as well
    f_out.close()

# this is called on execution --------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
    sys.exit()