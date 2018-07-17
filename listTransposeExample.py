"""
LIST TRANSPOSE
"""
__author__ = 'Sol Amour - amoursol@gmail.com'
__twitter__ = '@solamour'
__version__ = '1.0.0'

# NOTES: 
"""
Same as writing the following:
results = []
for x,y in zip(IN[0],IN1[]):
	results.append( [x, y] )	
"""


# Importing the CLR module
import clr

# The input ports
numbers = [ 1, 2, 3, 4, 5 ]
alphabet = [ "A", "B", "C", "D", "E" ]

# Running a map function to generate new lists (output) from our zipped dual list input
OUT = map(list, zip(numbers, alphabet))