"""
COLLECT CURVES BY LINE STYLE AND TYPE
"""
__author__ = 'Sol Amour - amoursol@gmail.com'
__twitter__ = '@solamour'
__version__ = '1.0.0'


# Importing Reference Modules
import clr # CLR ( Common Language Runtime Module )
clr.AddReference("RevitServices") # Adding the RevitServices.dll special Dynamo 
# module to deal with Revit
import RevitServices # Importing RevitServices
from RevitServices.Persistence import DocumentManager # From RevitServices import 
# the Document Manager
clr.AddReference("RevitAPI") # Adding the RevitAPI.dll module to access the Revit 
# API
import Autodesk # Here we import the Autodesk namespace
# From the Autodesk namespace - derived down to the Revit Database, we import only 
# the Filtered Element Collector and CurveElement classes
from Autodesk.Revit.DB import FilteredElementCollector, CurveElement

# Here we give the Revit Document a nickname of 'doc' which allows us to simply 
# call 'doc' later without having to type the long namespace name 
doc = DocumentManager.Instance.CurrentDBDocument

# We create a 'FilteredElementCollector' across the entire Revit Document and apply
# the 'OfClass' filter too it - returning only 'Curve Elements'
curves = FilteredElementCollector(doc).OfClass(CurveElement)


# We want to pull the Names of each curve and use a List Comprehension to do so. This
# will result in the creation of a list that contains all of the 'Curve Names' only
# and is itrated (ran across) our Filtered Element Collector list called 'curves'
lineType = [ crv.Name for crv in curves ]
# We want to also pull the Line Style Name for each curve and again use a List 
# Comprehension to do so. This results in the creation of a list that contains all of 
# the 'Line Style Names' for each curve in our 'curves' list
lineStyle = [ crv.LineStyle.Name for crv in curves ]

# We then want to pull ouch the unique names of each of our Line Style Names, so we
# call 'set' on the 'lineStyle' list. Set acts like List.UniqueItems inside of Dynamo
uniqueLineStyles = set(lineStyle)

# We then create two empty catchment lists, separated by commas
modelByStyle, detailByStyle = [], []

# Then we run a for loop for each of our unique Line Styles for every single 'item' 
# (Unique Line Style Name) inside of our 'uniqueLineStyles' list
for unique in uniqueLineStyles:
	# We run a List Comprehension across our zipped (paired) lists of 'curves', 
	# 'lineType' and 'lineStyle' (Note: Each of these lists MUST contain the same amount
	# of items for Zip to work), which will return each 'item' inside a new list if that
	# 'item' is of 'type' Model Lines and if it's 'style' matches the 'unique' variable
	# we are looping
	modelByStyle.append([ item for item, type, style in zip(curves, lineType, lineStyle) 
	if type == 'Model Lines' and style == unique ])
	# We run a List Comprehension across our zipped (paired) lists of 'curves', 
	# 'lineType' and 'lineStyle' (Note: Each of these lists MUST contain the same amount
	# of items for Zip to work), which will return each 'item' inside a new list if that
	# 'item' is of 'type' Detail Lines and if it's 'style' matches the 'unique' variable
	# we are looping
	detailByStyle.append([ item for item, type, style in zip(curves, lineType, lineStyle)
	if type == 'Detail Lines' and style == unique ])

# To get our results back inside of Dynamo, we need to append a list to 
# the OUT port. Here we append the Unique Line Styles, the list of 'Model Lines by Style'
# and the list of 'Detail Lines by Style'
OUT = uniqueLineStyles, modelByStyle, detailByStyle
