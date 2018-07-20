"""
PYTHON NUMBER SEQUENCE
"""
__author__ = 'Sol Amour - amoursol@gmail.com'
__twitter__ = '@solamour'
__version__ = '1.0.0'

# SYNTAX: [ value * step for value in range( amount ) ]
# Step = This is the value we will multiply our range by
# Amount = How many total values we want

# NOTES: 
# All parameters can be either integers or doubles
# All parameters can be positive or negative
# range( amount ) is the same as range( 0, amount )
# To achieve the same output as '0..10' in DesignScript, you must use 'range( 10 + 1 )' as the Stop value is not included in the range function

# The input ports
step = IN[0] # A number such as 20 (int) or 20.5 (float) demarcating the step
amount = IN[1] # A number such as 10 demarcating the amount

# The output port - In this case we use a list comprehension
OUT = [ value * step for value in range( amount ) ]