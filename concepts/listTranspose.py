"""
LIST TRANSPOSE EXAMPLE
"""
__author__ = 'Sol Amour - amoursol@gmail.com'
__twitter__ = '@solamour'
__version__ = '1.0.0'

# Our input list is tethered to the IN[0] port. This list contains a 2-dimensional list (Such as: {{ 1, 2, 3, 4}, {A, B, C, D}} )
inputList = IN[0]

# In order to transpose our lists, we will map the 'List' function across our 'unpacked' (Which is what the asterisk demarcates) zipped list 
OUT = map(list, zip(*inputList))
