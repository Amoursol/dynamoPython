'''
CREATE CEILING VIEW BY LEVEL, ROOMS
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

# import all classes from Revit DB
from Autodesk.Revit.DB import *
# import document manager
from RevitServices.Persistence import DocumentManager
# import transaction manager
from RevitServices.Transactions import TransactionManager
# instantiate current document
doc = DocumentManager.Instance.CurrentDBDocument

level = IN[0]
rooms = IN[1]
names = IN[2]
Offset = IN[3]/304.8
result = []

# make list
if not isinstance(rooms,list):
	Rooms = UnwrapElement([rooms])
else:
	Rooms = UnwrapElement(rooms)

if not isinstance(names,list):
	Names = [names]
else:
	Names = names

# create new bbox based on offset
def crop_box(bbox, offset):
	minX = bbox.Min.X - offset
	minY = bbox.Min.Y - offset
	minZ = bbox.Min.Z - offset
	maxX = bbox.Max.X + offset
	maxY = bbox.Max.Y + offset
	maxZ = bbox.Max.Z + offset
	
	newbox = BoundingBoxXYZ()
	newbox.Min = XYZ(minX,minY, minZ)
	newbox.Max = XYZ(maxX, maxY, maxZ)
	return newbox
	
# collect views
views = FilteredElementCollector(doc).OfClass(View).ToElements()
# get first ceiling view
cview = [v for v in views if v.ViewType == ViewType.CeilingPlan][0]

# start transaction
TransactionManager.Instance.EnsureInTransaction(doc)

# loop room and name
for room,name in zip(Rooms,Names):
	# duplicate ceiling view 
	view = cview.Duplicate(ViewDuplicateOption.WithDetailing)
	# get room bbox
	bbox = room.BoundingBox[doc.ActiveView]
	# create new bbox
	cbox = crop_box(bbox,Offset)
	# get duplicated view
	dupview = doc.GetElement(view)
	# set name
	dupview.Name = name
	# set view cropbox
	dupview.CropBox = cbox
	# set cropbox active
	dupview.CropBoxActive = True
	# set cropbox visibility
	dupview.CropBoxVisible = False
	# set scale
	dupview.Scale = 25
	# append result
	result.append(dupview)
# transaction done
TransactionManager.Instance.TransactionTaskDone()
# output result
OUT = result

