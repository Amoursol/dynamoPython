'''
CREATE DUCTS BY MODEL CURVES
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
from Autodesk.Revit.DB.Mechanical import *
# import transaction manager
from RevitServices.Transactions import TransactionManager

# instantiate current document
doc = DocumentManager.Instance.CurrentDBDocument

lines = IN[0]
ductType = UnwrapElement(IN[1])
ducts = []
# make list 
if isinstance(lines, list):
	lines = UnwrapElement(lines)
else:
	lines = UnwrapElement([lines])
#current view level
level = doc.ActiveView.GenLevel
#collect family symbol
fsymbol = FilteredElementCollector(doc).OfClass(MechanicalSystemType).ToElements()[0]

#transaction start
TransactionManager.Instance.EnsureInTransaction(doc)
# loop lines
for line in lines:	
	#create duct
	duct = Duct.Create(doc, fsymbol.Id,ductType.Id, level.Id, line.GeometryCurve.GetEndPoint(0), line.GeometryCurve.GetEndPoint(1));
	#append to result	
	ducts.append(duct)

#transaction end
TransactionManager.Instance.TransactionTaskDone()
# output result
OUT = ducts