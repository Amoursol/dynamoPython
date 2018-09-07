"""
SORT BY INDEX VALUE (REVERSED)
"""
__author__ = 'Sol Amour - amoursol@gmail.com'
__twitter__ = '@solamour'
__version__ = '1.0.0'

# SYNTAX: sorted( iterable, [ key = x, reverse = True ])
# Iterable = List to sort elements in
# Key = Key to use to sort the list of elements ( Optional )
# Reverse = Choice to reverse the sorting ( Optional )

# NOTES: 
# To utilise either the 'key' or 'reverse' optional parameters, 
# you must use the correct syntax of: key = x, or reverse = True
# Key can be a user defined function with which to sort


# Importing the Operator module
import operator

# The input port
plots = IN[0]

# Sorting our output list using the itemgetter operator which simply 
# states sort by indices in this order: Index 1 first, then index 2 
# second, then follow on with natural sorting afterwards
OUT = sorted( plots, key = operator.itemgetter( 1, 2 ), reverse = True )
