'''
Return part parameters values from Fabrication elements
'''

__author__ = 'Pablo Derendinger'
__twitter__ = '@pderen'
__version__ ='1.0.0'


# import common language runtime 
import clr

# clr.AddReference loads and imports .net assembly(dll) as python module
# load RevitAPI.dll 
clr.AddReference("RevitAPI")

# import all classes from Revit DB
from Autodesk.Revit.DB import *


#Fabrication elements
elements = IN[0]
#"Edit Part" parameter name
paramName = IN[1]

#If input is a single element, convert to list to iterate
if not isinstance(elements,list):
	elements = [elements]


def getFabParameter(element,name):
	'''Return the value of a dimension from Edit Part menu'''
	element = UnwrapElement(element)
	#Get all dimensions from "Edit Part"
	for dim in element.GetDimensions():
		#If dimension name match, look for the dimension value
		if dim.Name == name:
			return element.GetDimensionValue(dim)
 
#Listcomp calling the function getFabParameter
OUT= [getFabParameter(e,paramName) for e in elements]
