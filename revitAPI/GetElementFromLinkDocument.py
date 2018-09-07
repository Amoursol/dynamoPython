'''
FILTERED ELEMENT COLLECTOR - GET ELEMENTS FROM LINK DOCUMENTS
'''

__author__ = 'min.naung/mgjean @https://twentytwo.space/contact'
__twitter__ = '@_mgjean'
__version__ ='1.0.0'


# import common language runtime 
import clr

# import system to access enum class(line-34)
import System

# clr.AddReference loads and imports .net assembly(dll) as python module
# load RevitAPI.dll and RevitServices.dll
clr.AddReference("RevitAPI")
clr.AddReference("RevitServices")

# import filtered element collector and revit link instance classes
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, ElementCategoryFilter

# import document manager
from RevitServices.Persistence import DocumentManager

# instantiate current document
doc = DocumentManager.Instance.CurrentDBDocument

# excepted category object (input)
category = IN[0]

# convert category to BuiltInCategory
obj = System.Enum.ToObject(BuiltInCategory, category.Id)

# constructs a new instance of a filter to match elements by category
filter = ElementCategoryFilter(obj)

# collect elements that pass element category filter
collector = FilteredElementCollector(IN[1]).WherePasses(filter).WhereElementIsNotElementType().ToElements()

# return elements
OUT = collector
