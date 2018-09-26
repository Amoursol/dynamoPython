"""
REQUEST VIEW CHANGE - ASYNC METHOD
"""
__author__ = 'John Pierson - sixtysecondrevit@gmail.com'
__twitter__ = '@60secondrevit'
__version__ = '1.0.0'

# Importing Reference Modules
import clr # CLR ( Common Language Runtime Module )
clr.AddReference("RevitServices")# Adding the RevitServices.dll special Dynamo 
# module to deal with Revit
import RevitServices # Importing RevitServices
from RevitServices.Persistence import DocumentManager # From RevitServices 
# import the Document Manager
from RevitServices.Transactions import TransactionManager# From RevitServices 
# import the Transaction Manager

clr.AddReference("RevitAPI") # Adding the RevitAPI.dll module to access the Revit API
from Autodesk.Revit.DB import *

# here we give the Revit application a nickname of 'app' which allows us to use it to get the 'UIapp'. Which is the user interface application.
app = DocumentManager.Instance.CurrentUIApplication.Application
uiapp = DocumentManager.Instance.CurrentUIApplication

# User input view, unwrap to it's Revit.DB.Element representation
view = UnwrapElement(IN[0])
# output a result
output = []

# We need to force close Dynamo's open transaction to request the view change
TransactionManager.Instance.ForceCloseTransaction()

# try the view change, if it works do it and output the view, if not output an empty list.
try:
	# request view change as an async process
	uiapp.ActiveUIDocument.RequestViewChange(view)
	output = view
except:
	output = []

# Return the result
OUT = output