"""
FILTERED ELEMENT COLLECTOR
"""
__author__ = 'Sol Amour - sol.amour@designtech.io'
__twitter__ = '@solamour'
__copyright__ = 'designtech.io 2018'
__version__ = '1.0.0'


# Importing Reference Modules
import clr # CLR ( Common Language Runtime Module )
clr.AddReference("RevitServices") # Adding the RevitServices.dll special Dynamo module to deal with Revit
import RevitServices # Importing RevitServices
from RevitServices.Persistence import DocumentManager # From RevitServices import the Document Manager
clr.AddReference("RevitAPI") # Adding the RevitAPI.dll module to access the Revit API
import Autodesk # Here we import the Autodesk namespace
# From the Autodesk namespace - derived down to the Revit Database, we import only the Filtered Element Collector and BuiltInCategory classes
from Autodesk.Revit.DB import FilteredElementCollector

# Here we give the Revit Document a nickname of 'doc' which allows us to simply call 'doc' later without having to type the long namespace name 
doc = DocumentManager.Instance.CurrentDBDocument

# To create a Filtered Element Collector, we simply type the PINK part of RevitAPIDocs ( FilteredElementCollector ), wrap it inside of Parenthesis and then call the ORANGE part of RevitAPIDocs ( Document, View ). We are running multiple filters here: The 'OfClass', 'OfCategory' and 'Where Element Is Not Element Type'. We then cast it to Elements so we can use it in Dynamo.
elementCollector = FilteredElementCollector( doc ).WhereElementIsNotElementType().ToElements()

# To get our results back inside of Dynamo, we need to append a list to the OUT port
OUT = elementCollector