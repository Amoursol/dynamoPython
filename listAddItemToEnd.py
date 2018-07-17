"""
LIST: ADD ITEM TO END
"""
__author__ = 'Sol Amour - amoursol@gmail.com'
__twitter__ = '@solamour'
__version__ = '1.0.0'

# Input Lists
list01 = IN[0] # For example: list01 = [ 0, 1, 2, 3, 4 ]
list02 = IN[1] # For example: list02 = [ "A", "B", "C", "D", "E" ]

# Empty result lists
addedList, extendedList = [], [] # Generating empty 'catchment lists' to which we add our results

# Examples of Append
addedList.append(list01) # 'Append' will add, in it's entirety, list01 to the catchment list of 'addedList'
addedList.append(list02) # 'Append' will add, in it's entirety, list02 to the catchment list of 'addedList'

# Examples of Extend
extendedList.extend(list01) # 'Extend' will add, sans the outermost list, list01 to the catchment list of 'extendedList'
extendedList.extend(list02) # 'Extend' will add, sans the outermost list, list01 to the catchment list of 'extendedList'

# Output results
OUT = addedList, extendedList