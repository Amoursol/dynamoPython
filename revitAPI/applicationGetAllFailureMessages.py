
'''
GET ALL POSSIBLE FAILURE MESSAGES
'''
__author__ = 'john pierson'
__twitter__ = '@60secondrevit'
__version__ ='1.0.0'

# dynamo version - 1.3.3

# import common language runtime 
import clr

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices

# Import RevitAPI
clr.AddReference("RevitAPI")
# import all classes from Revit DB
from Autodesk.Revit.DB import *
# import document manager
from RevitServices.Persistence import DocumentManager
# import transaction manager
from RevitServices.Transactions import TransactionManager

# instantiate current document and application
doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

# obtain all failure message Revit.DB elements
failureDefinitions = app.GetFailureDefinitionRegistry().ListAllFailureDefinitions()

# declare a list to append descriptions to
failureDescriptions = []

# iterate through the failure definitions and append description to output
for i in failureDefinitions:
	failureDescriptions.append(i.GetDescriptionText())

# return the results
OUT = failureDescriptions