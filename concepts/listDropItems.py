"""
LIST: DROP ITEMS
"""
__author__ = 'Sol Amour - amoursol@gmail.com'
__twitter__ = '@solamour'
__version__ = '1.0.0'

# Input Lists
data = IN[0] # A data list such as: list01 = [ 0, 1, "hello", None, 17.5 ]
nums = IN[1] # A number (Positive or negative) of elements to drop from the list. 
# Positive drops from the start, negative drops from the end

# We run an 'If' conditional check here to see if we want to drop items from the 
# start or end of our list
if nums < 0:
	# If our number is less than zero (Such as '-2'), we drop elements from the 
	# end of the list through the following syntax: 
	# data[(start from the beginning) : cut to the negative index value backwards ]
	OUT = data[:nums] 
else:
	OUT = data[nums:] # Otherwise if our number is greater than zero (Such as '2'), 
	# we drop elements from the start of the list through the following syntax: 
	# data[ start from this index : (until the end of the list) ]
