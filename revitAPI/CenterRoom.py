'''
ROOM RELOCATE TO CENTER OF THE ROOM
'''
__author__ = 'min.naung/mgjean @https://twentytwo.space/contact'
__twitter__ = '@_mgjean'
__version__ ='1.0.0'

# dynamo version - 1.3.2 , 2.0.1

# import common language runtime 
import clr

# clr.AddReference loads and imports .net assembly(dll) as module
# load RevitAPI.dll and RevitServices.dll
clr.AddReference("RevitAPI")
clr.AddReference("RevitServices")
# import dynamo geometry classes
clr.AddReference('ProtoGeometry')

# import RevitNodes for geometry conversion
# convert dynamo to revit vice versa
clr.AddReference("RevitNodes")
# import system and revit
import System,Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

# import geometry class and point class from dynamo geometry
from Autodesk.DesignScript.Geometry import (Geometry,
Point as pt)

# import all classes from Revit DB
from Autodesk.Revit.DB import *
# import document manager
from RevitServices.Persistence import DocumentManager
# import transaction manager
from RevitServices.Transactions import TransactionManager
# instantiate current document
doc = DocumentManager.Instance.CurrentDBDocument


# input[0] 
elems = IN[0]

# make list
if not isinstance(elems,list):
	elems = UnwrapElement([elems])
else:
	elems = UnwrapElement(elems)

# output
res = []
# start transaction
TransactionManager.Instance.EnsureInTransaction(doc)

# loop elements
for e in elems:
	# level elevation - unit millimeter 
	elevation = e.Level.Elevation * 304.8
	# get geo-objects of the element
	geoelem = e.GetGeometryObjectFromReference(Reference(e))
	# get enumerator to loop geo-objects
	geoobj = geoelem.GetEnumerator()
	# loop geo-objector
	for obj in geoobj:
		# convert to dynamo type
		room_geometry = obj.ToProtoType()
		# get the centroid of the element
		point = room_geometry.Centroid()
		# create location point with level elevation
		center = pt.ByCoordinates(point.X,point.Y,elevation)
		# current element location
		current = e.Location.Point
		# point convert to revit and minus from current location
		newloc = center.ToXyz() - current
		# move to new location
		e.Location.Move(newloc)

# transaction done
TransactionManager.Instance.TransactionTaskDone()

# output
OUT = elems
