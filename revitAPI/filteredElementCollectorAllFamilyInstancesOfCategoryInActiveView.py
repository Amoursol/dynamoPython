"""
FILTERED ELEMENT COLLECTOR
"""
__author__ = 'Sol Amour - amoursol@gmail.com'
__twitter__ = '@solamour'
__version__ = '1.0.0'


# Importing Reference Modules
import clr # CLR ( Common Language Runtime Module )
clr.AddReference("RevitServices") # Adding the RevitServices.dll special 
# Dynamo module to deal with Revit
import RevitServices # Importing RevitServices
from RevitServices.Persistence import DocumentManager # From RevitServices 
# import the Document Manager
clr.AddReference("RevitAPI") # Adding the RevitAPI.dll module to access 
# the Revit API
import Autodesk # Here we import the Autodesk namespace
# From the Autodesk namespace - derived down to the Revit Database, we 
# import only the Filtered Element Collector and BuiltInCategory classes.
# The use of \ allows us to return a chained function on a new line without
# throwing an error.
from Autodesk.Revit.DB import FilteredElementCollector, \
BuiltInCategory, FamilyInstance

# Here we give the Revit Document a nickname of 'doc' which allows us to 
# simply call 'doc' later without having to type the long namespace name 
doc = DocumentManager.Instance.CurrentDBDocument

# We create a 'Filtered Element Collector' that will collect, in the 
# 'Active View' of our document, all 'Family Instances' of a particular 
# category ('Planting'). We then cast it to Elements so we can use it in 
# Dynamo.
# The use of \ allows us to return a chained function on a new line without
# throwing an error.
builtInCollector = FilteredElementCollector(doc, doc.ActiveView.Id) \
    .OfClass(FamilyInstance) \
    .OfCategory(BuiltInCategory.OST_Planting) \
    .WhereElementIsNotElementType() \
    .ToElements()

# To get our results back inside of Dynamo, we need to append a list to 
# the OUT port
OUT = builtInCollector
