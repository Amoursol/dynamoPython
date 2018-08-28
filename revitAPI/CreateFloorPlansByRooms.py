'''
CREATE FLOOR PLAN VIEW BY ROOMS, LEVEL
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

# check list for rooms
if isinstance(IN[0], list):
	rooms = UnwrapElement(IN[0])
else:
	rooms = [UnwrapElement(IN[0])]
# check list for name
if isinstance(IN[1],list):
	names = IN[1]
else:
	names = [IN[1]]

# level input
level = UnwrapElement(IN[2])
# offset from room bbox (mm to ft)
offset = IN[3]/304.8

def crop_box(bbox, offset):
	# modify x,y,z point of bbox
	minX = bbox.Min.X - offset
	minY = bbox.Min.Y - offset
	minZ = bbox.Min.Z - offset
	maxX = bbox.Max.X + offset
	maxY = bbox.Max.Y + offset
	maxZ = bbox.Max.Z + offset
	# create new bbox
	newbox = BoundingBoxXYZ()
	newbox.Min = XYZ(minX,minY, minZ)
	newbox.Max = XYZ(maxX, maxY, maxZ)
	return newbox

# collect view type in document
viewTypes = FilteredElementCollector(doc).OfClass(ViewFamilyType)
#loop view types
for i in viewTypes:
	# floor plane view type
	if i.ViewFamily == ViewFamily.FloorPlan:
		# get type id
		viewTypeId = i.Id
		# break the loop
		break
# start transaction
TransactionManager.Instance.EnsureInTransaction(doc)
# output list		
floorPlans = []
# loop rooms and names together
for i,name in zip(rooms,names):
	# level id
	levelId = level.Id
	# get bounding box
	bbox = i.BoundingBox[doc.ActiveView]
	# create new bounding vox
	newBbox = crop_box(bbox, offset)
	# create floor plan view
	newView = ViewPlan.Create(doc, viewTypeId, levelId)
	# set view name
	newView.ViewName = name
	# set cropbox to newbbox
	newView.CropBox = newBbox
	# set cropbox active
	newView.CropBoxActive = True
	# set visibility
	newView.CropBoxVisible = False
	# set view scale
	newView.Scale = 50
	# append output 
	floorPlans.append(newView)
	
# End Transaction
TransactionManager.Instance.TransactionTaskDone()
# output 
OUT = floorPlans
