"""
PYTHON RANGE: DOUBLE APPROACH
"""
__author__ = 'Sol Amour - amoursol@gmail.com'
__twitter__ = '@solamour'
__version__ = '1.0.0'

# DEFINITION:
# Custom definition to build a function similar to our DesignScript float range
def floatRange( start, end, step ):
	for number in xrange( end ):
		yield start
		start += step

# SYNTAX: floatRange( [start], stop[, step ] )
# Start = Starting number of the sequence [Open]
# Stop = Generate numbers up to, but not including this number [Closed]
# Step = Difference between each number in the sequence. In order to pair with our DesignScript variant, we need to run this as: ( 1.0 / end)

# NOTES: 
# If we wish to use floating values (Doubles) we have to specify, hence in our step value we use 1.0 instead of 1. IF we used 1 (An integer) we would simply return a list of zeroes

# The input ports
start = IN[0] # A number such as 0 (int)
end = IN[1] # A number such as 10 (int)

# A divisor calculation that changes our ints to floats
step = ( 1.0 / end )

# The output port - In this case a list comprehension
OUT = [ value for value in floatRange( start, end + 1, step ) ]
