"""
LIST: MINIMUM AND MAXIMUM ITEMS
"""
__author__ = 'Sol Amour - amoursol@gmail.com'
__twitter__ = '@solamour'
__version__ = '1.0.0'

"""

SYNTAX: min(iterable[, key = x])

min = Return the smallest item in an iterable or the smallest of two or more arguments
iterable = An iterable element (Such as a list, tuple, dictionary)
[,key] = An optional 'key' argument to specificy how to find the minimum argument

"""


dataSingle = [ 1, 2, 3, 4, 5 ] # A data list of numbers
dataDouble = [["A", 11], ["B", 7], ["C", 9]] # A data list of lists (Paired alphabetic 
# and numeric characters)

minimumItem = min(dataSingle) # Will return the lowest natural sort item of '1'
maximumItem = max(dataSingle) # Will return the highest natural sort item of '5'

minimumItemKey = min(dataDouble, key = lambda d : d[1] ) # Will return the middle pairing of 
# '["B", 7]' as we use an anonymous function (Lambda) as our key that simple states we're parsing 
# the 'minimum item' based off Index 1 (Our numbers)
maximumItemKey = max(dataDouble, key = lambda d : d[1] ) # Will return the first pairing of 
# '["A", 11]' as we use an anonymous function (Lambda) as our key that simple states we're parsing 
# the 'maximum item' based off Index 1 (Our numbers)

OUT = minimumItem,maximumItem,minimumItemKey,maximumItemKey
