"""
dir explorer
-
a dynamoPython script, visit the website for more details
https://github.com/Amoursol/dynamoPython
"""

__author__ = 'Adam Bear - adam@ukbear.com'
__twitter__ = '@adambear82'
__github__ = '@adambear82'
__version__ = '1.0.0'

"""
Explore the attributes in a reference using the built in dir() function
"""

import clr

# add the reference to explore
clr.AddReference('DSCoreNodes')
import DSCore

# its normal to import the contents of the reference with an asterik
# for all or to import individually,
# here we dont actually need them so is commented out
# from DSCore import *

# reference to explore with dir
ref = DSCore

# create empty list & dictionary
dirAll = []
dic = {}

for key in dir(ref) :
    # create string of attribute
    dir_str = getattr(ref, key)

    # list all ref dir
    dirAll.append(dir(dir_str))

    # for each key
    for value in dirAll :
        # assign value to key in dic
        dic[key] = value

# output the unsorted dictionary
OUT = dic
