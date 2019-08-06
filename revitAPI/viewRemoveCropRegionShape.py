"""
VIEW REMOVE CROP REGION SHAPE
"""
__author__ = 'Sol Amour - amoursol@gmail.com'
__twitter__ = '@solamour'
__version__ = '1.0.0'


# Importing Reference Modules
import clr # CLR ( Common Language Runtime Module )
clr.AddReference("RevitServices") # Adding the RevitServices.dll special Dynamo 
# module to deal with Revit
import RevitServices # Importing RevitServices
from RevitServices.Persistence import DocumentManager # From RevitServices import 
# the Document Manager
from RevitServices.Transactions import TransactionManager  # From RevitServices 
# import the Document Manager
clr.AddReference("RevitAPI") # Adding the RevitAPI.dll module to access the Revit 
# API
import Autodesk # Here we import the Autodesk namespace
# From the Autodesk namespace - derived down to the Revit Database, we import only 
# the Filtered Element Collector and CurveElement classes
from Autodesk.Revit.DB import FilteredElementCollector, CurveElement

# Here we give the Revit Document a nickname of 'doc' which allows us to simply 
# call 'doc' later without having to type the long namespace name 
doc = DocumentManager.Instance.CurrentDBDocument

# We want to access the Revit API on our 'view' objects, so we have to Unwrap them
# to get under the hood. If we do not Unwrap the views, we only have access to the
# DynamoAPI calls on the object. To do this, we simply wrap our IN[0] port inside
# of the 'UnwrapElement()' function
viewList = UnwrapElement(IN[0])

# If the view doesn't have the attribute of '__iter__' (Which means iterable - i.e 
# it's an object that contains objects such as a 'List') then we want to wrap that 
# singular item (In our case a view) into a List of one thing. This way our For 
# Loop will never fail due to rank
if not hasattr(viewList, '__iter__'):
	# By adding square braces around the variable of 'view' we put it inside a
	# new list
	viewList = [viewList]

# Creating an empty catchment list for our Success/Failure messages
message = []

# To affect the Revit model we have to wrap all of our API calls inside a 
# Transaction. This is Revit's way of handling content change and is called by the
# Dynamo service .dll called 'RevitServices'. What this means is we wrap all of our
# Dynamo changes into a single Transaction (Instead of having a LOT of things to 
# undo with Ctrl + Z in our 'back' log inside of Revit) called 'Dynamo-GUID script'
TransactionManager.Instance.EnsureInTransaction(doc)

# We run 'Try/Except' error handling to stop the node execution if any part of the
# 'try' indented code returns a None (null)
try:
	# We then must run a 'For Loop' across every view (item) inside our viewList (list)
	# that allows us to make changes to either a single view, or multiple views when
	# fed in inside Dynamo
	for view in viewList:
		# We first do a conditioanl check. 'If' the view property of 'CropBoxActive' is
		# on (True) then, and only then, do the following
		if view.CropBoxActive == True:
			# Query the Crop Region Shape Manager applied to the view we are checking
			# against and give it a variable name of 'cropManager'
			cropManager = view.GetCropRegionShapeManager()
			# After we have access to our Crop Region Shape Manager (cropManager) then 
			# we can call a method (action) on that manager to 'Remove Crop Region
			# Shape' by using the API call of 'RemoveCropRegionShape()'
			cropManager.RemoveCropRegionShape()
			# If successful, we append the view
			message.append( view )
		# Otherwise if the view does not have a Crop Box Active
		else:
			# If unsuccessful, we append a None (null)
			message.append( None )
			
# If our 'try' statement fails by returning a None (null), then execute the following 
# code instead		
except:
	# Import the 'sys' module to capture System Specific Parameters
	import sys
	# Append to the 'path' list a string where the Python interpreter can look for 
	# non-native modules
	sys.path.append(r'C:\Program Files (x86)\IronPython 2.7\Lib')
	# Import the 'traceback' module to capture Error messages from the appended path
	import traceback
	# Set our output message as the formatted failure message from the 'traceback'
	# module
	message = traceback.format_exc()
	

# After we have affected the Revit Model we close the Transaction which allows
# Revit to be accessed again (If in a worksharing environment) and that Transaction
# to be undone if needed through Ctrl + Z
TransactionManager.Instance.TransactionTaskDone()

# If our message list contains only a singular item we don't need it to be wrapped up
# inside a list. So we check if the len (count) of our list is greather than or equal
# to 1 and then, and only then, do we change our output from 'message' (A list) to 
# 'message[0]', the first item in that list. There is no 'else' check as the default
# list of 'message' is acceptable and the 'If' statement won't execute if that 
# condition doesn't exist
if len(message) >= 1:
	message = message[0]

# To get our results back inside of Dynamo, we need to append our 'message'
# the OUT port
OUT = message
