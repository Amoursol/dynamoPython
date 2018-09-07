'''
roundDoublesAsStrings - AS A FIXED (NOT FLOATING) POINT
'''
__author__ = 'Adam Bear - adam@ukbear.com'
__twitter__ = '@adambear82'
__version__ = '1.0.0'

# ------------------------
# inputs
# ------------------------

# check if IN[0] has any values
if IN[0] :
	# set values of numbers using IN[0]
	numbers = IN[0]

# if IN[0] does not have any values
else :
	# set numbers to this list to get started with
	numbers = (
	(6395.1145038168, -7837.1501722652, 100),
	(9239.11844170387, -5285.31979606026, 300)
	)

# ------------------------
# format specification
# ------------------------

# an empty list to store our results in
roundNumbers = []
# an empty list to store values for chopping lists into slices
subLists = []

# refer to docs on format specification
# https://docs.python.org/2.7/library/string.html#format-specification-mini-language

# the number of digits to round to
digits = 11
# the number of digits to round to as a string
# prefixed with '.' and suffixed with 'f' for fixed (not floating) point
# prefixed with % as a specifier
# eg to format % with specification for fixed point of 11 digits
# formatSpec = '%.11f'
formatSpec = '%' + '.' + str(digits) + 'f'

# for every instance in list numbers
for n0 in numbers :
	# set initail value for counter of items in sub list
	subList = 0

	# including items in nested lists
	for n1 in n0 :

		# use format specification to format a specificer, n1
		# note in this context % is not being used to find modulo
		# % represents the start of the specifier, n1
		formatted = formatSpec % n1

		# append formatted values to roundNumbers list
		roundNumbers.append(formatted)

		# if we were happy to accept a flat list we could stop here
		# but if we want to preserve the sublists that were inputted
		# first we need to count the number of items in each sublist
		# later on we will chop the roundNumbers by those values
		# add one to the current subList counter value
		subList += 1

	# for each outer loop append counter value of inner loop
	subLists.append(subList)

# ------------------------
# chop list
# ------------------------

def ListChopUnevenly(chopList, chopLengths) :
# to output the numbers in the same sub list nesting as it was inputed
# clockwork provides a good example of how to chop lists unevenly
# annotated with kudos from
# https://github.com/andydandy74/ClockworkForDynamo/blob/master/nodes/1.x/List.Chop%2B.dyf
# define the function with variables

	# create an empty list to return values from
	chopped = []
	# set an initail value for a counter
	count = 0
	# find the length of the list to be chopped
	max = len(chopList)

	# for each item in chopLengths
	for num in chopLengths :

		# check if counter has reached the length of the chopList
		if count + num > max :

			# set the end value as length of the chopList
			end = max

		# if counter has not reached the length of the chopList
		else :

			# set the end value as the count + num
			# eg count plus current value in chopLengths loop
			end = count + num

		# after checking above if and else conditions then
		# slice the chopList between count and end
		sliced = chopList[count:end]
		# append the sliced list to chopped
		chopped.append(sliced)
		# set the count value to end value for next loop
		count = end

	# when all loops complete return sliced list of chopped values
	return chopped

# chop the roundNumbers by the subLists
choppedNumbers = ListChopUnevenly(roundNumbers, subLists)

# ------------------------
# OUT
# ------------------------

# send the choppedNumbers list to the OUT port
OUT = choppedNumbers
