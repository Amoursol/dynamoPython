"""
LIST: CHUNKING
"""
__author__ = 'Sol Amour - amoursol@gmail.com'
__twitter__ = '@solamour'
__version__ = '1.0.0'

# Example of Chunking (Grouping an item with its next)
def chunks(list, number):  # Requires a list and a number
	for index in range(0, len(list), number):  # For every
		# index inside of a number range starting at '0' 
		# and running to the length of the list, with steps
		# of a chosen 'number'
		yield list[index : index + number]  # Yield returns
		# a 'generator' object, so we cast the result to a
		# 'list' and will return 'list slices' ranging from
		# the chosen 'index' to the chosen 'index' + chosen
		# 'number'

# Exemplar list
itemList = [0, 1, 2, 3, 4, 5]  # A simple list of numbers to
# parse with our 'chunks' definition

count = 2 # A number which we want to chunk to. We choose '2'
# which will result in sublists of: [[0, 1], [2, 3], [4,5]]

chunksList = chunks(itemList, count)  # Here we call our new
# 'chunks' definition on our 'itemList' and with our 'count' 
# then push those results to our variable called 'chunksList'

OUT = chunksList  # Returning our chunked data

