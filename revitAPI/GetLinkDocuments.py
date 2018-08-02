'''
FILTERED ELEMENT COLLECTOR - GET LINK DOCUMENTS
'''

__author__ = 'min.naung/mgjean @https://twentytwo.space/contact'
__twitter__ = '@_mgjean'
__version__ ='1.0.0'


# import common language runtime 
import clr

# clr.AddReference loads and imports .net assembly(dll) as python module
# load RevitAPI.dll and RevitServices.dll
clr.AddReference("RevitAPI")
clr.AddReference("RevitServices")

# import filtered element collector and revit link instance classes
from Autodesk.Revit.DB import FilteredElementCollector, RevitLinkInstance

# import document manager
from RevitServices.Persistence import DocumentManager

# instantiate current document
doc = DocumentManager.Instance.CurrentDBDocument

# collect link documents from current document
link_docs = FilteredElementCollector(doc).OfClass(RevitLinkInstance)

# return ["link document name","link document"] list-structure for each link documents
OUT = [[i.Name.split(":")[0],i.GetLinkDocument()] for i in link_docs]
