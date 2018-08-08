"""
COMPARISON OPERATORS
"""
__author__ = 'Sol Amour - amoursol@gmail.com'
__twitter__ = '@solamour'
__version__ = '1.0.0'

greaterThan = 10 > 5  # Is '10' greater than '5' ? Evaluates to True
greaterThanOrEqualTo = 10 >= 10  # Is '10' greater than or equal to '10' 
# ? Evaluates to True
lessThan = 5 < 10  # Is '5' less than '10' ? Evaluates to True
lessThanOrEqualTo = 5 <= 5  # Is '5' less than or equal to '5' ? Evaluates 
# to True
equals = 5 == 5  # Does '5' equal '5' ? Evaluates to True
notEquals = 5 != 10  # Does '5' not equal '10' ? Evaluates to True

x = 2  # Assinging the variable of 'x' a value of '2'
y = 1 < x < 3  # Is '1' less than 'x' (2) is less than 3 ? Evaluates to True

OUT = [greaterThan, greaterThanOrEqualTo, lessThan, lessThanOrEqualTo,
equals, notEquals, y]
