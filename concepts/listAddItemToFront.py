"""
LIST: ADD ITEM TO FRONT
"""
__author__ = 'Sol Amour - amoursol@gmail.com'
__twitter__ = '@solamour'
__version__ = '1.0.0'

"""

SYNTAX: List.insert(index, item)

List = The list to which you want to insert an item
.insert = The insert function which requires two input variables
index = The index where you wish to insert your new item
item = The item which you wish to insert into your list

"""


insertItem = [ "X", 3 ] # A list of elements to insert
baseList = [["A", 11], ["B", 7], ["C", 9]] # A data list of lists (Paired alphabetic and 
# numeric characters)

baseList.insert(0, insertItem) # We want to insert our 'insertItem' into our 'baseList', 
# so we call the function '.insert' on our 'baseList' and choose an index of '0' 
# (Add Item to Front)

OUT = baseList
