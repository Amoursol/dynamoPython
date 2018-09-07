'''
CREATE ISOMETRIC VIEWS BY SECTION VIEWS
'''
__author__ = 'min.naung/mgjean @https://twentytwo.space/contact'
__twitter__ = '@_mgjean'
__version__ ='1.0.0'

# dynamo version - 1.3.2

# import common language runtime 
import clr

# clr.AddReference loads and imports .net assembly(dll) as python module
# load RevitAPI.dll and RevitServices.dll
clr.AddReference("RevitAPI")
clr.AddReference("RevitServices")
# load dynamo geometry
clr.AddReference('ProtoGeometry')
# load revit nodes for geometry conversion
clr.AddReference("RevitNodes")
# import revit elements and conversion
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

# import dynamo geometry for geometry objects
from Autodesk.DesignScript.Geometry import *
# imoprt revit-api-db classes
from Autodesk.Revit.DB import (FilteredElementCollector,
ViewFamilyType,ViewFamily,View3D,BoundingBoxXYZ)

# import document manager
from RevitServices.Persistence import DocumentManager
# import transaction manager
from RevitServices.Transactions import TransactionManager
# instantiate current document
doc = DocumentManager.Instance.CurrentDBDocument

# collect view type
collector = FilteredElementCollector(doc).OfClass(ViewFamilyType)
# get 3DViewType
for i in collector:
	# collect 3DView family
	if i.ViewFamily == ViewFamily.ThreeDimensional:
		viewType = i
		break

# create a function
def SectionToIsometric(view):
	mgr = view.GetCropRegionShapeManager()
	# curves 
	curve = mgr.GetCropShape()
	# direction of section
	vector = view.ViewDirection.ToVector().Reverse()
	# view extend
	offset = view.LookupParameter("Far Clip Offset").AsDouble()*304.8
	points = []
	for i in curve[0]:
		# start point of each curve
		start = i.GetEndPoint(0).ToPoint()
		# make list
		points.append(start)
	# create polycurve
	curves = PolyCurve.ByPoints(points,True)
	# curve extrude by direction and distance , result as solid
	solid = Curve.ExtrudeAsSolid(curves,vector,offset)
	# create bbox
	bbox = BoundingBox.ByGeometry(solid).ToRevitType()
	# create 3dview
	view3d = View3D.CreateIsometric(doc,viewType.Id)
	# view name includes (3D)
	view3d.ViewName = view.ViewName + " (3D)"
	# set cropbox size to bbox size
	view3d.CropBox = bbox
	# set cropbox active
	view3d.CropBoxActive = False
	# cropbox visibility
	view3d.CropBoxVisible = True
	# set sectionbox to bbox
	view3d.SetSectionBox(bbox)
	# set view scale
	view3d.Scale = 50
	# return view
	return view3d

# input views
views = IN[0]
# output result
result = []
# check list 
if not isinstance(views,list):
	views = UnwrapElement([views])
else:
	views = UnwrapElement(views)
# start transaction
TransactionManager.Instance.EnsureInTransaction(doc)
# loop views
for view in views:
	# call function with view is an argument
	result.append(SectionToIsometric(view))
# transaction end
TransactionManager.Instance.TransactionTaskDone()
# output result
OUT = result