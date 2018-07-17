"""
MEMBERSHIP / BOOLEAN OPERATORS
"""
__author__ = 'Sol Amour - amoursol@gmail.com'
__twitter__ = '@solamour'
__version__ = '1.0.0'

# Default list
list = [ 1, 2, 3, 4 ]

inCheck = 4 in list # Membership check to see if the number '4' is 'in' our default list: Results in True as membership test is true
notInCheck = 4 not in list # Membership check to see if the number '4' is 'not' 'in' our default list: Results in False as the 'not' operator flips the boolean result. Our number '4' is in the list

andCheck = inCheck and notInCheck # The 'And' boolean operator evaluates to True if and only if both checks are True
orCheck = inCheck or notInCheck # The 'Or' boolean operator evaluates to True if any of the checks evaluates to True

OUT = inCheck, notInCheck, andCheck, orCheck