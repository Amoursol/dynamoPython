'''
CREATE THREE-D VIEW BY ROOMS AND NAMES
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

rooms = IN[0]
names = IN[1]
offset = IN[2]/304.8  # mm to ft
results = []

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
	
def createNewSectionBox(elem,viewName,offset):
	# collect view type in document
	viewTypes = FilteredElementCollector(doc).OfClass(ViewFamilyType)
	#loop view types
	for i in viewTypes:
		# floor plane view type
		if i.ViewFamily == ViewFamily.ThreeDimensional:
			# get type id
			viewTypeId = i.Id
			# break the loop
			break
	# create new bbox by current bbox and offset
	bbox = crop_box(elem.BoundingBox[doc.ActiveView],offset)
	
	# create 3D View
	view = View3D.CreateIsometric(doc, viewType.Id)
	# set view name
	view.Name = viewName
	# set sectionbox to bbox
	view.SetSectionBox(bbox)
	# set cropbox active
	view.CropBoxActive = True
	# set cropbox visibility
	view.CropBoxVisible = True
	# set view scale
	view.Scale = 50
	# set detail level to fine
	view.DetailLevel = ViewDetailLevel.Fine
	# set detail style to shading
	view.DisplayStyle = DisplayStyle.Shading
	# return view
	return view

# start Transaction
TransactionManager.Instance.EnsureInTransaction(doc)
# loop element and name together
for element,name in zip(rooms,names):
	# call function with element, name and offset arguments
	# and append it to results
	results.append(createNewSectionBox(element,name,offset))
	
# end Transaction
TransactionManager.Instance.TransactionTaskDone()
# output results
OUT = results

