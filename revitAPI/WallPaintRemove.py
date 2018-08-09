'''
WALLS - REMOVE PAINT FROM WALLS 
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

# input wall elements
walls = IN[0]

# check input is list or not
if not isinstance(walls, list):
	walls = UnwrapElement([walls])
else:	
	walls = UnwrapElement(walls)

# start transaction
TransactionManager.Instance.EnsureInTransaction(doc)

# loop input elements
for i in walls:
	
	# get geometry object (solid)
	geoelem = i.GetGeometryObjectFromReference(Reference(i))
	
	# solid to geometry object
	geoobj = geoelem.GetEnumerator()
	
	# loop geometry object
	for obj in geoobj:
	
		# collect faces from geometry object
		for f in obj.Faces:
		
			# get each face
			doc.RemovePaint(i.Id,f)
			
#end of transaction		
TransactionManager.Instance.TransactionTaskDone()
			
# output result
OUT = walls
