'''
DOCUMENT - RELOAD ALL LINK DOCUMENTS 
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

# collect link documents
links = FilteredElementCollector(doc).OfClass(RevitLinkInstance).ToElements()

# create empty list for OUT(retrun)
load = []

# input is true
if IN[0]:
	# loop links list
	for link in links:
		#get link type document
		linkType  = doc.GetElement(link.GetTypeId())
		#get link document saved filepath
		filepath = linkType.GetExternalFileReference().GetAbsolutePath()
		try:
			# try to reload from saved filepath
			linkType.LoadFrom(filepath,None)
			# append to OUT(return)
			load.append(linkType)
		except:
			# if can't load from saved filepath
			# return info showing that this link not found on saved filepath
			load.append(link.Name.split(" : ")[0]+" <File Not Found>")
			pass
	OUT = load

# if false (or) none input
else:
	# input true to run
	OUT="Set true to run!"
