
"""
HELPERS: CONVERT INPUT TO LIST
"""
__author__ = 'John Pierson - sixtysecondrevit@gmail.com'
__twitter__ = '@60secondrevit'
__version__ = '1.0.0'
"""
Since we are typically building our python scripts to work over a list of items, 
# it is very important to account for it in our code within Python. Often times 
# Dynamo will give you a single item and Python will not know what to do with it 
# if it is expecting a list. The below def will allow for this conversion.
"""

# Importing Reference Modules
import clr # CLR ( Common Language Runtime Module )
clr.AddReference("RevitServices") # Adding the RevitServices.dll special Dynamo 
# module to deal with Revit
import RevitServices # Importing RevitServices
from RevitServices.Persistence import DocumentManager # From RevitServices import 
# the Document Manager
from RevitServices.Transactions import TransactionManager # From RevitServices 
# import the Transaction Manager

# Here we give the Revit Document a nickname of 'doc' which allows us to simply 
# call 'doc' later without having to type the long namespace name 
doc = DocumentManager.Instance.CurrentDBDocument

# Custom method to convert single items to a list to iterate over, also unwraps 
# the items.
def toList(x): # the name of the function
	if isinstance(x,list): return UnwrapElement(x) # if the input element is 
	# a single thing, return it as a list. 
	else : return [UnwrapElement(x)] # if the input thing was a list all 
	# along, just return that

# The input ports
element = toList(IN[0]) # Convert the input to a list (if necessary).

OUT = element # simply output the new list for this example
