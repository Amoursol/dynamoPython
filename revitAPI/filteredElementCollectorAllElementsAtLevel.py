"""
FILTERED ELEMENT COLLECTOR
"""
__author__ = 'Sol Amour - amoursol@gmail.com'
__twitter__ = '@solamour'
__version__ = '1.0.0'


# Importing Reference Modules
import clr # CLR ( Common Language Runtime Module )
clr.AddReference("RevitServices") # Adding the RevitServices.dll special Dynamo module to deal with Revit
import RevitServices # Importing RevitServices
from RevitServices.Persistence import DocumentManager # From RevitServices import the Document Manager
clr.AddReference("RevitAPI") # Adding the RevitAPI.dll module to access the Revit API
import Autodesk # Here we import the Autodesk namespace
from Autodesk.Revit.DB import FilteredElementCollector, Wall, ElementId, ElementLevelFilter # From the Autodesk namespace - derived down to the Revit Database, we imoprt only the Filtered Element Collector, Wall, ElementId and ElementLevelFilter classes

# Here we give the Revit Document a nickname of 'doc' which allows us to simply call 'doc' later without having to type the long namespace name 
doc = DocumentManager.Instance.CurrentDBDocument

# Here we create a a filter based on the a chosen Level - input via our Input Port
filter = ElementLevelFilter( Autodesk.Revit.DB.ElementId( IN[0].Id ) )

# We then run a 'Filtered Element Collector' with our created 'filter' (Chosen Level), and discount any element that is an 'Element Type' before using the 'ToElements' call to return real elements.
elementAtLevelCollector = FilteredElementCollector( doc ).WherePasses( filter ).WhereElementIsNotElementType().ToElements()

# To get our results back inside of Dynamo, we need to append a list to the OUT port
OUT = elementAtLevelCollector
