"""
PYTHON NUMBER RANGE
"""
__author__ = 'Sol Amour - amoursol@gmail.com'
__twitter__ = '@solamour'
__version__ = '1.0.0'

# SYNTAX: range( [start], stop[, step ] )
# Start = Starting number of the sequence [Open]
# Stop = Generate numbers up to, but not including this number [Closed]
# Step = Difference between each number in the sequence

# NOTES: 
# All parameters must be integers
# All parameters can be positive or negative
# range(10) is the same as range(0,10)

# The input port
start = IN[0] # A start Number such as 0 (int)
stop = IN[1] # A stop Number such as 10 (int)
step = IN[2] # A step Number such as 2 (int)

rangeStopDefined = range( stop ) # This will be similar to the DesignScript 
# variant minus one: '0..(stop - 1)'
rangeStopDefinedDesignScript = range( stop + 1 ) # This mimics the DesignScript 
# variant of '0..stop'
rangeStartStopStep = range( start, stop, step ) # This will give us a number range 
# with a defined start, stop and step similar to the DesignScript variant minus 
# one: '0..10-1..2'
rangeStartStopStepDesignScript = range( start, stop + 1, step ) # THis mimics the 
# DesignScript variant of '0..10..2'

# The output port
OUT = rangeStopDefined, rangeStopDefinedDesignScript, rangeStartStopStep, 
rangeStartStopStepDesignScript
