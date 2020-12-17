
'''
GET ALL POSSIBLE FAILURE MESSAGES
'''
__author__ = 'john pierson - sixtysecondrevit@gmail.com'
__twitter__ = '@60secondrevit'
__github__ = '@sixtysecondrevit'
__version__ ='1.0.0'

# dynamo version - 2.6.0
# originally made to answer https://forum.dynamobim.com/t/room-location-point-of-a-family-the-green-dot/58480/2

# import common language runtime 
import clr

# Import RevitAPI
clr.AddReference("RevitAPI")
# import all classes from Revit DB
from Autodesk.Revit.DB import *

# import Revit dynamo libraries
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

# custom definition for location that works with single items or lists
def GetLocation(item):
	# if it has a calculation point return that
	if item.HasSpatialElementCalculationPoint : return item.GetSpatialElementCalculationPoint().ToPoint()
	# if not return the regular location
	elif item.Location.GetType().ToString().Contains("LocationPoint") : return item.Location.Point.ToPoint()

	else: return None

# the family instances
items = UnwrapElement(IN[0])

# return the results
if isinstance(IN[0], list): OUT = [GetLocation(x) for x in items]
else: OUT = GetLocation(items)
