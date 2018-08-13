'''
WHILE TRUE - APPEND SUMMED VALUE FROM SEQUENCE WHILE CONDITIONS MET
'''
__author__ = 'Adam Bear - adam@ukbear.com'
__twitter__ = '@adambear82'
__version__ = '1.0.0'

# --------------------------
# Importing Reference Modules
# --------------------------

# CLR ( Common Language Runtime Module )
import clr
# importing the sys module allows the importing of other modules
import sys

# this is the default location of the python library
pythonPath = 'C:\\Program Files (x86)\\IronPython 2.7\\Lib'
# '\\' is used in the path as '\' needs to be escaped by '\'
# its common to use 'r' as a prefix for a raw string literal
# and then only use single '\' for file paths
# 'r' ignores all escapes and works fine in a python node
# but will not work in a python from string node

# appending pythonPath allows the modules in that path to be imported
sys.path.append(pythonPath)
# change the output port OUT to see a list of
# OUT = sys.builtin_module_names

# importing random will give access to the random module
import random

# --------------------------
# explore the random module with dir and doc
# --------------------------

# change the output port OUT to see random documentation
# OUT = random.__doc__

# change the output port OUT to to see its directory
# OUT = dir(random)

# we can see one of the defined functions is called choice
# change the output port OUT to see its documentation
# OUT = random.choice.__doc__

# opening random.py from the pathonPath we can see the defintion finds
# the length of the sequence multiplies this by a random number and
# uses this value to get a single item at random index in the sequence
# seq [ random * len(seq) ]
# change the output port OUT to see a randomly slected value
# OUT = random.choice((0, 1))

# --------------------------
# while True
# --------------------------

# establish some check values
# unlike design script python boolean values have Capital Lettters
checkA = True
checkB = True
checkC = True

# list of integers to be selected from (0,1)
addValues = range(2)
# an initail value for summed values is zero
sum = 0
# create an empty list to store output values
output = []

# (True) could be replaced with a boolean if neccesary
while True :
	# set value i randomly from addValues
	i = random.choice(addValues)
	# set value of sum, as sum + i
	sum += i
	# when the value of sum is greater or equall to 5
	if sum >= 5 :
		# append to output within the if loop
		output.append('next value is greater or equall to 5')
		# stop evaluating through the while loop
		break

	# check else if any of the booleons (checkA & checkB) are not True
	elif any ( [ not checkA, not checkB ] ) :
	# the not all statement is more compact but makes less sense
	# elif not all ( [ checkA, checkB ] ) :
		# append to output within the else if loop
		output.append('checkA and/or checkB is False')
		# stop evaluating through the while loop
		break

	# check if the checkC boolean is not True
 	elif not checkC :
		# append to output within the else if loop
 		output.append('this will print on every other line')
		# by using the pass statement the next elif is ignored
 		pass

	# check else if sum equalls 2
 	elif sum == 2 :
		# append to output within the else if loop
 	 	output.append('two')
		# by using the continue statement the while loop is not broken, but
		# output.append(sum) outside of the else if is not executed
 		continue

	# append the sum value to the output list,
	# unless else if with continue is True
	output.append(sum)

# --------------------------
# send the output sequence to the OUT port
# --------------------------
OUT = output
