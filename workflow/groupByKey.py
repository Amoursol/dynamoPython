"""
GROUP BY KEY
"""
__author__ = 'Sol Amour - amoursol@gmail.com'
__twitter__ = '@solamour'
__version__ = '1.0.0'


# The input ports
elements = IN[0]
keys = IN[1]

# The set function is the same as List.UniqueItems in Dynamo and is 
# sorted by default
uniqueKeys = set(keys)

# We create an empty results list to capture our elements
results = []

# We run a 'For Loop' over all of our unique key values
for uniqueItem in uniqueKeys:
	# Here we generate a sublist so we can match our sphere radius 
	# together and append that entire group into our results list
	keyGroup = []
	# We then run a comparison check using two lists: Our elements list 
	# and our keys list. We do this using the 'zip function', which 
	# simply means shortest lacing. Inside of this comparison we run a 
	# 'For Loop'
	for element, key in zip(elements,keys):
		# For every single value of inside our Keys list, if it matches 
		# the unique key value...
		if key == uniqueItem:
			# Then append its paired Element to the sublist called 
			# KeyGroup
			keyGroup.append(element)
	# After we have ran through and matched every single Element that matches
	# our first unique key value, we append that element
	results.append(keyGroup)

# We will iterate across every single unique key value in turn and append the Elements in groups to our results list
OUT = results
