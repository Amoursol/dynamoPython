"""
PYTHON GET ITEM AT INDEX
"""
__author__ = 'Sol Amour - amoursol@gmail.com'
__twitter__ = '@solamour'
__version__ = '1.0.0'

# SYNTAX: list[ index ]
# index = This is the index integer you want to pull a value from

# NOTES: 
# All parameters have to be integers and can be positive or negative
# Negative integers will take items from the last item backwards
# You have to use either a For loop or List Comprehension to get 
# items from a series of indices

# The input port elements
numbers = [ 0, 1, 2, 3, 4, 5, 6 7, 8, 9, 10 

getItemAtIndex = numbers[ 3 ] # Getting the item at a specified index
getLastItem = numbers[ -1 ] # Getting the last item in a list
getLastItemPopMethod = numbers.pop() # Getting the last item in a list 
# using the 'pop' method

# The out port using our sublist queries
OUT = getItemAtIndex, getLastItem, getLastItemPopMethod
