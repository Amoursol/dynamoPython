"""
PYTHON LIST SLICING: FLAT LIST
"""
__author__ = 'Sol Amour - amoursol@gmail.com'
__twitter__ = '@solamour'
__version__ = '1.0.0'

# SYNTAX: [ startCut : endCut ]
# startCut = This is the first item included in the Slice
# endCut = This is the last item included in the Slice

# NOTES: 
# All parameters have to be integers
# A colon is required to demarcate slicing
# The first value is the start point. If left empty, it starts at the beginning
# The second value is the end point. If left empty, it takes the entire list from the chosen start point
# Using -1 at the end will give the second to last item in a list. Using -X will come backwards from the end of the list (i.e -2 finishes the Slice at the third to last item)
# A slice of list[ : ] will clone the list

# A multi-tiered numbers list
numbers = [ [ 0, 1, 2, 3 ], [ 4, 5, 6, 7, 8 ] ]

chosenRangeInSublists = [ n[ 1 : -1 ] for n in numbers ] # Using a List Comprehension to get all items from the 1st index to the second to last index in all sublists


# The out port using our List Slices
OUT = chosenRangeInSublists