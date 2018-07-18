"""
LIST: REPLACE NULLS (SINGLE LIST)
"""
__author__ = 'Sol Amour - amoursol@gmail.com'
__twitter__ = '@solamour'
__version__ = '1.0.0'


data = ["a", None, 17.1, 3, "C", "X", None, 4] # A mixed list of data types inclusive of nulls (None's)
replacementItem = 'I\'m not a None' # A replacement item (Note: The backslash is an 'Escape Character' that allows us to use an apostrophe inside of a string)

results = [] # An empty container list to which we will append (Add to) our results

for item in data: # A 'For' loop that we run over the entire list (data) of inputs
	if item is not None: # A conditional check that says: "If an item in the list called 'data' 'is not None' (That is - is valid) - simply add it to our output list"
		results.append(item) # If the conditional check is sucessful, then append that element to our container list called 'results'
	else: # If the item IS a null (None), then do the following
		results.append(replacementItem) # If the conditional check fails, then append our replacement element to our container list called 'results' in the place of the None at the same index
		
OUT = results
