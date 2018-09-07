'''
COPY AND PASTE FILTERS - VIEW TO VIEWS
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

# view to copy
viewtocopy= UnwrapElement(IN[0])
# views to paste
viewstopaste = IN[1]
# make list
if not isinstance(viewstopaste,list):
	viewstopaste = UnwrapElement([IN[1]])
else:
	viewstopaste = UnwrapElement(IN[1])

# start transaction
TransactionManager.Instance.EnsureInTransaction(doc)
# views to paste loop each view
for view in viewstopaste:
	# views to copy loop each filter id
	for id in viewtocopy.GetFilters():
		# set filter override
		view.SetFilterOverrides(id,viewtocopy.GetFilterOverrides(id))
		# set filter visibility
		view.SetFilterVisibility(id,viewtocopy.GetFilterVisibility(id))
		
# transaction done		
TransactionManager.Instance.TransactionTaskDone()

# output views
OUT = viewstopaste
