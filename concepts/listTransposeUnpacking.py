"""
LIST TRANSPOSE (UNPACKING MATRIX)
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


# The input ports
numbers = [1, 2, 3, 4, 5]
alphabet = ["A", "B", "C", "D", "E"]

matrix = [numbers, alphabet]

# Here we create a list of the zip function being called on our matrix. 
# We need to prefix the list with an asterisk ( * ) which tells our zip 
# function to unpack (Remove the outer list) of our matrix. Without this 
# we would be calling zip( [ [0,1,2,3,4], ['a','b','c','d','e'] ] ) which 
# will cause zip to fail. If we utilise the asterisk, it unpacks the outer 
# list resulting in: zip( [0,1,2,3,4], ['a','b','c','d','e'] ) which will 
# correctly execute
OUT = list(zip(*matrix))
