'''
ROOM COLLECTION WITH ROOM STATUS
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

# if provided input[0]
if IN[0]:
	rooms = UnwrapElement(IN[0])
	
# if no input, collect all rooms
else:
	# collect all rooms 
	rooms = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms)
	rooms = rooms.ToElements()

# room status list for output
placed,notplaced,notenclosed,redundant = [],[],[],[]

# loop rooms
for r in rooms:
	# get room boundary need one argument(opts)
	s = r.GetBoundarySegments(SpatialElementBoundaryOptions())
	# get location of room
	l = r.Location
	# if location is none
	if l == None:
		# append to not placed
		notplaced.append(r)
	# elif no boundary segments
	elif len(s)<1:
		# append to not enclosed
		notenclosed.append(r)
	# elif area zero
	elif r.Area == 0:
		# append to redundant
		redundant.append(r)
	# passed all conditions
	else:
		# append to placed
		placed.append(r)

OUT = placed,notplaced,notenclosed,redundant