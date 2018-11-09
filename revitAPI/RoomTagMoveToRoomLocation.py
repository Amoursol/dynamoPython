'''
ROOM TAGS RELOCATE TO ROOM LOCATION 
'''

__author__ = 'min.naung/mgjean @https://twentytwo.space/contact'
__twitter__ = '@_mgjean'
__version__ ='1.0.0'


# import common language runtime 
import clr

# clr.AddReference loads and imports .net assembly(dll) as python module
# load RevitAPI.dll and RevitServices.dll
clr.AddReference("RevitAPI")
clr.AddReference("RevitServices")

# import Revit DB classes
from Autodesk.Revit.DB import * 

# import document manager
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

# instantiate current document
doc = DocumentManager.Instance.CurrentDBDocument

# collect room tags from active view
collector = FilteredElementCollector(doc, doc.ActiveView.Id)
tags = collector.OfClass(SpatialElementTag).ToElements()

# start transaction
TransactionManager.Instance.EnsureInTransaction(doc)

# loop tags
for i in tags:
	# get room location 
	room_loc = i.Room.Location.Point
	# location to move (room location - current tag location)
	new_loc = room_loc - i.Location.Point
	# move to new location
	i.Location.Move(new_loc)

# end transaction
TransactionManager.Instance.TransactionTaskDone()
# output
OUT = tags
