"""
LIST: FLATTEN A LIST
"""
__author__ = 'Pablo Derendinger - pderendinger@gmail.com'
__twitter__ = '@pderen'
__version__ = '1.0.0'


#List of Lists
list_Of_List_Regular = [[1,2,3],[4,5,6],[7,8,9]]

list_Of_List_Irregular = [[1,2,[1,2,3]],[4,5,6],[7,8,9]]

#flatten a list with list comprehension, elegant but this works 
#only for 1 leve List of Lists 
#https://coderwall.com/p/rcmaea/flatten-a-list-of-lists-in-one-line-in-python
flat_List1 = [item for sublist in list_Of_List_Regular for item in sublist]

#Flatten an irregular list of list with a function 
#stackoverflow.com https://bit.ly/2MxA2Ro

def flatten(L):
    for item in L:
        try:
            yield from flatten(item)
        except TypeError:
            yield item

flat_List2 = flatten(list_Of_List_Irregular)

OUT = flat_List1, flat_List2
