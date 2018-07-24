'''
FILTERED ELEMENT COLLECTOR - ALL_MODEL_MARK ELEMENTS ONLY
'''
__author__ = 'Adam Bear - adam@ukbear.com'
__twitter__ = '@adambear82'
__version__ = '1.0.0'

# Importing Reference Modules
# CLR ( Common Language Runtime Module )
import clr
# Adding the RevitServices.dll special Dynamo module to deal with Revit
clr.AddReference('RevitServices')
import RevitServices  # Importing RevitServices
# From RevitServices import the Document Manager
from RevitServices.Persistence import DocumentManager
# Adding the RevitAPI.dll module to access the Revit API
clr.AddReference('RevitAPI')
import Autodesk  # Here we import the Autodesk namespace
# From the Autodesk namespace - derived down to the Revit Database
# we import only the required classes
from Autodesk.Revit.DB import \
FilteredElementCollector, BuiltInParameter, \
ParameterValueProvider, ElementId, FilterStringBeginsWith, \
FilterStringContains, FilterStringEndsWith, FilterStringEquals, \
FilterStringGreater, FilterStringGreaterOrEqual, FilterStringLess, \
FilterStringLessOrEqual, FilterStringRule, ElementParameterFilter
# to import all classes use the wildcard '*'
# this will marginally slow down dynamo/python and may cause errors if
# multiple classes are identically named
# from Autodesk.Revit.DB import *

# Here we give the Revit Document a nickname of 'doc'
# which allows us to simply call 'doc' later without 
# having to type the long namespace name 
doc = DocumentManager.Instance.CurrentDBDocument
# similary FilteredElementCollector is shortened to fec
fec = FilteredElementCollector

# Here we use the Built In Parameter method to choose the string parameter
# of 'ALL_MODEL_MARK' across all Elements inside of the Revit Document
# refer to api docs for all built in parameter enumarations
# http://www.revitapidocs.com/2018.1/fb011c91-be7e-f737-28c7-3f1e1917a0e0.htm
param = BuiltInParameter.ALL_MODEL_MARK

# Once we have our BuiltInParameter, we need to get it's Element Id
# and convert it to a Parameter Value Provider
# in order to use it inside of our filter
provider = ParameterValueProvider(ElementId(param))

# refer to api docs for available evaulators
# http://www.revitapidocs.com/2016/b317951e-6324-fc45-5860-6b616534d1ce.htm?query=filter%20string%20class
evalBegins = FilterStringBeginsWith()
evalCon = FilterStringContains()
evalEnds = FilterStringEndsWith()
evalEq = FilterStringEquals()
evalGreat = FilterStringGreater()
evalGoEq = FilterStringGreaterOrEqual()
evalLess = FilterStringLess()
evalLoEq = FilterStringLessOrEqual()
# Here we select which evaluator will be used to test against a set value
# whilst maintaining the list of other filters for reference
evaluator = evalBegins

# Does the mark string contain the test value 'M.'
test = 'begins'

# booleon (True/False) controls if test is case sensitive
caseSensitive = False

# we run a Filter String Rule that checks the chosen parameter
# 'ALL_MODEL_MARK' runs against the evaluator (does this string)
# contain  our test string value 'M.'
# refer to api docs for details of the FilterStringRule Constructor
# http://www.revitapidocs.com/2015/056fd8e1-a989-b262-8c8e-9e79ece62b01.htm
rule = FilterStringRule(provider, evaluator, test, caseSensitive)

# generate a filter based off our Rule
filter = ElementParameterFilter(rule)

# Now we have a valid rule to run against our Filtered Element Collector.
# # So in this case we pull everything inside the document
# but only if it passes our filter test
# then make sure we return the elements themselves with '.ToElements()'
analyticalCollector = fec(doc).WherePasses(filter).ToElements()

# To get our results back inside of Dynamo
# we need to append a list to the OUT port
OUT = analyticalCollector
