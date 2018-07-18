"""
LIST: REMOVE NULLS (SINGLE LIST)
"""
__author__ = 'Sol Amour - amoursol@gmail.com'
__twitter__ = '@solamour'
__version__ = '1.0.0'


data = ["a", None, 17.1, 3, "C", "X", None, 4] # A mixed list of data types inclusive of nulls (None's)

results = [] # An empty container list to which we will append (Add to) our results

for item in data: # A 'For' loop that we run over the entire list (data) of inputs
	if item is not None: # A conditional check that says: "If an item in the list called 'data' 'is not None' (That is - is valid) - simply add it to our output list, otherwise pass to the next item"
		results.append(item) # If the conditional check is sucessful, then append that element to our container list called 'results'
		
OUT = results
