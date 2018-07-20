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

# A basic numbers list
numbers = [ 0, 1, 2, 3, 4, 5, 6 ]

chosenStartToEnd = numbers[ 3 : ] # Getting all numbers from the 3rd index until the end of the list
startToChosenEnd = numbers[ : 5 ] # Getting all numbers up to the 5th index in the list
chosenStartToSecondToLastItem = numbers[ 3 : -1 ] # Getting all number sfrom the 3rd index to the second to last item

# The out port using our List Slices
OUT = chosenStartToEnd, startToChosenEnd, chosenStartToSecondToLastItem