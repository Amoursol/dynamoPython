"""
ELEMENT PRE-DELETE
"""
__author__ = 'Oliver Green - oliveredwardgreen@gmail.com'
__twitter__ = 'Oliver_E_Green'
__version__ = '1.0'

"""This script prompts the user to select an element in Revit.
It will then run (but not commit) a transaction to delete this element.
The transaction is rolled-back - but we are able to get the ElementIds
of all of the elements which WOULD have been deleted had this transaction
been committed. We can use the ElementIds to see which elements
are dependent on the user-specified element."""

import clr #We import the Common Language Runtime
import sys
sys.path.append('C:\Program Files (x86)\IronPython 2.7\Lib')
#Importing the standard IronPython class library
import System
from System import Array
#We import some standard data collections from System
from System.Collections.Generic import *

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

clr.ImportExtensions(Revit.GeometryConversion)

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")
import Autodesk
from Autodesk.Revit.DB import *
#from Autodesk.Revit.DB import Transaction
from Autodesk.Revit.UI.Selection import * 
#We need to import the Selection class from Autodesk's UI library
#This will let us access Revit's element selection mode.

doc = DocumentManager.Instance.CurrentDBDocument
#Assign a short alias to the currently-open Revit document.
uiapp = DocumentManager.Instance.CurrentUIApplication
#An alias to the currently-open Revit UI application.
uidoc = uiapp.ActiveUIDocument
#An alias for the currently-open Revit UI document.
app = uiapp.Application
#An alias for the currently-open Revit UI application.

refresh = IN[0]
#An optional toggle to refresh this code.
#Connect this to a boolean toggle in Dynamo.

element_ids = [] #We create an empty list to store element ids.
elements = [] #We create an empty list for storing elements.

if refresh == True or refresh == False:
	#This condition is purely used to let the node refresh via the boolean toggle.
	selection = uidoc.Selection
	#We assign Revit's UI document selection class to the
	#Alias 'selection' for ease of use.
	reference = selection.PickObject(ObjectType.Element, "Select Element to Delete")
	#We assign the term 'reference' to Revit's PickObject method.
	#This prompts the user to select a Revit element.
	
	deleted_ids = list([ElementId])
	#We create a new empty list for storing element ids
	#This syntax is Ironpython to create a type-safe or 'generic' list.
	
	#We begin, then roll-back the transaction
	t = Transaction(doc, 'Name') #We name our transaction 't' 
	t.Start() #Transaction starts
	deleted_ids = doc.Delete(reference.ElementId)
	#We use Revit's delete method to temporarily
	#Delete the user-specified element
	#And store the ids of the subsequently-deleted
	#Items in our type-safe list.
	t.RollBack()
	#We do not commit the transaction.
	#Instead it is rolled-back and nothing is deleted in the Revit document.
	
	if not t.HasEnded:
		#Just in case the transaction refuses to end
		#We call Revit's Dispose method.
		#This deletes the transaction we created.
		t.Dispose()	
	string = "Object Selected: {}".format(reference.ElementId)
	#We create a report string to inform the user
	#Of the Id of the element they selected.

#Formatting a list of Element IDs the way Revit accepts them
for id in deleted_ids:
	element_ids.append(id.ToString())
	#We iterate through the elements which would have been deleted
	#If the user had deleted their indicated element
	#We store their ElementIds in a list.
	elements.append(doc.GetElement(id))
	#We also add each element which would
	#have been deleted to a different list.

OUT = string, elements, ";".join(element_ids)
#We output the report string, followed by the list of elements
#Which would have been deleted and a semicolon-separated list
#Of these elements' ElementIds.
#This list can be useful when using Revit's 'Select by Id' tool.
