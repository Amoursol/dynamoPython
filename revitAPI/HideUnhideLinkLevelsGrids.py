'''
HIDE / UNHIDE - LEVELS AND GRIDS FROM LINKS DOCUMENTS
'''
__author__ = 'min.naung/mgjean @https://twentytwo.space/contact'
__twitter__ = '@_mgjean'
__version__ ='1.0.0'

# dynamo version - 1.3.2 , 2.0.1

# import common language runtime 
import clr

# clr.AddReference loads and imports .net assembly(dll) as module
# load RevitAPI.dll and RevitServices.dll
clr.AddReference("RevitAPI")
clr.AddReference("RevitServices")

# import system for dotnet List
import System
from System.Collections.Generic import List

# import all classes from Revit DB
from Autodesk.Revit.DB import *
# import document manager
from RevitServices.Persistence import DocumentManager
# import transaction manager
from RevitServices.Transactions import TransactionManager
# instantiate current document
doc = DocumentManager.Instance.CurrentDBDocument

# start transaction
TransactionManager.Instance.EnsureInTransaction(doc)

# active view
active_view = doc.ActiveView

# filter name "can name anything"
ifilter = "GiveFilterAName"

endWiths = "Anything"

# filter check
found = False

# input[0] boolean
hide = False if IN[0] else True

# collect all filter elements
allFilters = FilteredElementCollector(doc).OfClass(FilterElement).ToElements()

# get filters from current view
viewFilters = active_view.GetFilters()
# collect filters' names
viewFiltersName = [doc.GetElement(i).Name.ToString() for i in viewFilters]

# loop each filter
for fter in allFilters:
	# filter already have in doc but not in current view
	if ifilter == fter.Name.ToString() and ifilter not in viewFiltersName:
		# add filter
		active_view.AddFilter(fter.Id)
		# set filter visibility
		active_view.SetFilterVisibility(fter.Id, hide)
		found = True
	# filter already have in doc and current view
	if ifilter == fter.Name.ToString() and ifilter in viewFiltersName:
		# set filter visibility
		active_view.SetFilterVisibility(fter.Id, hide)
		found = True
		
# if filter not found in doc
if not found:
	# all grids in doc
	grids = FilteredElementCollector(doc).OfClass(Grid).ToElements()
	# all levels in doc
	levels = FilteredElementCollector(doc).OfClass(Level).ToElements()
	# collect category id from grid and level
	CateIds = List[ElementId]([grids[0].Category.Id,levels[0].Category.Id])
	
	# type ids from grids 
	gridTypeIds = set([i.GetTypeId() for i in grids])
	# type ids from levels
	levelTypeIds = set([i.GetTypeId() for i in levels])
	
	# get grid type element
	type_elems = [doc.GetElement(i) for i in gridTypeIds]
	# get level type element
	type_elems.extend([doc.GetElement(l) for l in levelTypeIds])
	
	# loop type elements
	for elem in type_elems:
		# if endwiths not include in type name
		if not endWiths in elem.LookupParameter("Type Name").AsString():
			# add endwiths in type name
			elem.Name = elem.LookupParameter("Type Name").AsString() + endWiths
	# get type names
	type_names = [i.LookupParameter("Type Name").AsString() for i in type_elems]
	# type name parameter id
	paramId = type_elems[0].LookupParameter("Type Name").Id
	# create a "not ends with" filter rule
	notendswith = ParameterFilterRuleFactory.CreateNotEndsWithRule(paramId,endWiths,False)
	# create parameter filter element
	paramFilterElem = ParameterFilterElement.Create(doc, ifilter,CateIds,[notendswith])
	# set filter overrides (same with add filter to current)
	active_view.SetFilterOverrides(paramFilterElem.Id, OverrideGraphicSettings())
	# set filter visibility
	active_view.SetFilterVisibility(paramFilterElem.Id, hide)
	
# transaction done
TransactionManager.Instance.TransactionTaskDone()

# output
OUT = "DONE!"
