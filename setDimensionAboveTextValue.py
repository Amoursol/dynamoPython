"""
SET DIMENSION ABOVE TEXT
"""
__author__ = 'Sol Amour - amoursol@gmail.com'
__twitter__ = '@solamour'
__version__ = '1.0.0'


# Importing Reference Modules
import clr # CLR ( Common Language Runtime Module )
clr.AddReference("RevitServices") # Adding the RevitServices.dll special Dynamo module to deal with Revit
import RevitServices # Importing RevitServices
from RevitServices.Persistence import DocumentManager # From RevitServices import the Document Manager
from RevitServices.Transactions import TransactionManager # From RevitServices import the Transaction Manager

# Here we give the Revit Document a nickname of 'doc' which allows us to simply call 'doc' later without having to type the long namespace name 
doc = DocumentManager.Instance.CurrentDBDocument


# The input ports 
dimensions = UnwrapElement(IN[0]) # Here we 'unwrap' our Dynamo objects. Dynamo and Revit Elements are different - Dynamo has wrapped them up in order to manipulate them so for us to use them in the actual Revit Project we need to unwrap them so that we can talk to the Revit API
text = IN[1] # As this input is simply text we do not need to unwrap it

# Wrapping the body of our code inside of Transactions. This allows us to effect the Revit Project ( Document ).
TransactionManager.Instance.EnsureInTransaction(doc) # We have to be inside of a Transaction to manipulate the Revit Project so we use the Dynamo Specific transaction wrapper ( A special way to use the Transaction Class ) to ensure we are in a transaction. This way, if anything goes wrong inside of our script the Manager will ensure nothing breaks, that any partial changes made are reverted and that our Revit file is cleaned up before progressing

# We generate an empty catchment list to append (add to) our results
results = []

# We then run a For Loop across every single element that is coming into our 'dimensions' input node
for dim in dimensions: # For every single dimension inside of our input list called 'dimensioins', do the following...
	numOfSegs = dim.NumberOfSegments # Count the amount of Segments the Dimensions has
	if numOfSegs > 0: # Run an 'If' conditional check to see if it has more than zero (Which in turn means it's Segmented). If the answer to this check is True (It's either True or False) then do the following...
		for num in range(numOfSegs): # Create a Number Range starting at zero and ranging to the total count of our Number of Segments
			dim.Segments[num].Above = str(text) # Then for every segmented Dimension, change each Segments 'Above' property ( Which refers to the Text Field entitled 'Above inside of the Dimensions editor ), at each index ( Supplied by our variable num ), to our chosen Text value from our Input port
			results.append(dim) # Then simply append ( add ) this dimension to our empty catchment list 'results'
	else:
		dim.Above = str(text) # Set the property called 'Above' ( Which refers to the Text Field entitled 'Above' inside of the Dimensions editor ) to our chosen text from our second input port
		results.append(dim) # Then simply append ( add ) this dimension to our empty catchment list 'results'

TransactionManager.Instance.TransactionTaskDone() # After we have our script body finish executing, we want to close our Transaction. So we once again use the wrapper to close the Transaction using the 'TransactionTaskDone()' method

# The output port, showcasing the Revit Documents Saved Name
OUT = results