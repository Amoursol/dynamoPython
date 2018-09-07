'''
CONTINOUSLY ADD 1
'''
__author__ = 'Adam Bear - adam@ukbear.com'
__twitter__ = '@adambear82'
__version__ = '1.0.0'

# dynamo will only recalculate nodes which have changed inputs between
# runs, for the most part this is a very useful feature that speeds up
# calculation times in dyanmo, if only a small part changes then only
# that small part needs to be recalcualted.

# when dynamo is set to run automatically if the inputs to a python node
# have not changed then the python node will not be recaulated. To force
# the recalcuation on a python node it is common to include a bool
# toggle input to 'refresh' the inputs so the python node is
# re-calculated by dynamo

# when dynamo is set to run periodically inputting a DateTime.Now node
# into the python node forces the python node to be reavaluated every
# time. Be carefull to set the periodic interval to a time greater than
# the whole graph to be evaluated, otherwise dynamo will 'freeze'
nowNode = IN[0]

# set a location for a temp file that will be used as a counter
tempStringCounter = 'C:\\Temp\\tempStringCounter.txt'
# try to open the above tempStringCounter
try :
	# refer to tempStringCounter as file to be 'r' read
	# using 'with' will automatically close the file when finished with
	with open(tempStringCounter, 'r') as file :
		# read the value of the file
		value = file.read()
		# if the file does not have a value (blank) then
		if not value :
			# set the initial value of counterPlusOne as 0 in python
			counterPlusOne = 0
		# if the file does have a value then
		else :
			# convert the text value string into a float then integer
			counter = int(float(value))
			# +1 to the counter in each run of the python script
			counterPlusOne = counter + 1
	# refer to tempStringCounter as file to be 'w' written
	# using 'with' will automatically close the file when finished with
	with open(tempStringCounter, 'w') as file :
		# write the counterPlusOne value to the file
		file.write(str(counterPlusOne))

# if not able to open tempStringCounter then
except :
	# create tempStringCounter
	# using 'with' will automatically close the file when finished with
	with open(tempStringCounter, 'w') as file :
		# write the value '0' in the tempStringCounter
		file.write('0')
		# set the initial value of counterPlusOne as 0 in python
		counterPlusOne = 0

# an output that changes from 0 to 9999.... is not very useful
# specify an end value that after which the value should return to zero
end = 10
# use the modulus operator '%' to find the remainder of the division
index = counterPlusOne % end
# for the range of letters a to j
letters = 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'
# this can then be used as the index to a list in python or dynamo
output = letters[index]
# send the output to the OUT port
OUT = index, output
