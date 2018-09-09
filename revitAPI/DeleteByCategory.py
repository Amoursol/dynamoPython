'''
DELETE ELEMENTS BY CATEGORY
'''
__author__ = 'min.naung/mgjean @https://twentytwo.space/contact'
__twitter__ = '@_mgjean'
__version__ ='1.0.0'

# dynamo version - 1.3.2

# import common language runtime 
import clr

# clr.AddReference loads and imports .net assembly(dll) as python module
# load RevitAPI.dll and RevitServices.dll
clr.AddReference("RevitAPI")
clr.AddReference("RevitServices")

# import system 
import System

# import all classes from Revit DB
from Autodesk.Revit.DB import *
# import document manager
from RevitServices.Persistence import DocumentManager
# import transaction manager
from RevitServices.Transactions import TransactionManager
# instantiate current document
doc = DocumentManager.Instance.CurrentDBDocument

# input category
cat = IN[0]

# output list
res =[]

# get category object
obj = System.Enum.ToObject(BuiltInCategory, cat.Id)

# create category filter by category object
filter = ElementCategoryFilter(obj)

# collect filtered elements by category
elements = FilteredElementCollector(doc).WherePasses(filter).WhereElementIsNotElementType().ToElements()

# transaction start
TransactionManager.Instance.EnsureInTransaction(doc)

# loop elements
for elem in elements:
	try:
		# delete from document
		r = doc.Delete(elem.Id)
		# deleted id append to output
		# after deleted its return as a elementId list 
		# what we want is elementId only, so use [0]
		res.append(r[0])
	except:
		# error message append to output
		res.append("ElementID %s can't delete." %elem.Id)
		continue
	
# transaction end
TransactionManager.Instance.TransactionTaskDone()
# output result
OUT = res