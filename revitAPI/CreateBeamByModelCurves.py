'''
CREATE BEAM - BY MODEL CURVES
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

# import all classes from Revit DB
from Autodesk.Revit.DB import *

# import document manager
from RevitServices.Persistence import DocumentManager
# import transaction manager
from RevitServices.Transactions import TransactionManager

# instantiate current document
doc = DocumentManager.Instance.CurrentDBDocument

# input model curves
lines = IN[0]
# empty list for return output
beams = []

# if input is a list 
if isinstance(lines, list):
	lines = UnwrapElement(lines)
# if not a list
else:
	lines = UnwrapElement([lines])

#current view level
level = doc.ActiveView.GenLevel

#collect family symbol
fsymbol = FilteredElementCollector(doc).OfClass(FamilySymbol)

#collect first symbol from structural framing symbols
sym=fsymbol.OfCategory(BuiltInCategory.OST_StructuralFraming).ToElements()[0]

#transaction start
TransactionManager.Instance.EnsureInTransaction(doc)

for line in lines:
	
	#create beam
	beam = doc.Create.NewFamilyInstance(line.GeometryCurve, sym, 
		level, Structure.StructuralType.Beam)
	#append to output
	beams.append(beam)

#transaction end
TransactionManager.Instance.TransactionTaskDone()

#output
OUT = beams
