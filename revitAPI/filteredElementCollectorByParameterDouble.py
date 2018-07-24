'''
FILTERED ELEMENT COLLECTOR - CURVE_ELEM_LENGTH
'''
__author__ = 'Adam Bear - adam@ukbear.com'
__twitter__ = '@adambear82'
__version__ = '1.0.0'

# Importing Reference Modules
# CLR ( Common Language Runtime Module )
import clr
# Adding the RevitServices.dll special Dynamo module to deal with Revit
clr.AddReference('RevitServices')
# Importing RevitServices
import RevitServices
# From RevitServices import the Document Manager
from RevitServices.Persistence import DocumentManager
# Adding the RevitAPI.dll module to access the Revit API
clr.AddReference('RevitAPI')
import Autodesk  # Here we import the Autodesk namespace
# From the Autodesk namespace - derived down to the Revit Database
# we import only the required classes
from Autodesk.Revit.DB import \
FilteredElementCollector, BuiltInParameter, ParameterValueProvider, \
ElementId, FilterNumericEquals, FilterNumericGreater, \
FilterNumericGreaterOrEqual, FilterNumericLess, \
FilterNumericLessOrEqual, FilterDoubleRule, ElementParameterFilter
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

# Here we use the Built In Parameter method to choose the double parameter
# of 'CURVE_ELEM_LENGTH' across all Elements inside of the Revit Document
# refer to api docs for all built in parameter enumarations
# http://www.revitapidocs.com/2018.1/fb011c91-be7e-f737-28c7-3f1e1917a0e0.htm
param = BuiltInParameter.CURVE_ELEM_LENGTH

# Once we have our BuiltInParameter, we need to get it's Element Id
# and convert it to a Parameter Value Provider
# in order to use it inside of our filter
provider = ParameterValueProvider(ElementId(param))

# refer to api docs for available evaulators
# http://www.revitapidocs.com/2016/13cab7f3-d15d-adfd-ff43-c69a4863a636.htm?query=Filter%20Numeric%20class
evaluatorEq = FilterNumericEquals()
evaluatorGr = FilterNumericGreater()
evaluatorGoEq = FilterNumericGreaterOrEqual()
evaluatorLess = FilterNumericLess()
evaluatorLoEq = FilterNumericLessOrEqual()
# Here we select which evaluator will be used to test against a set value
# whilst maintaining the list of other filters for reference
evaluator = evaluatorGr

# length value tested against double (1234.567 mm = 4.050 ft)
mm = 1234.567
feet = mm * 0.00328084
test = feet

# rounding at which two doubles are considered equal
epsilon = 10**-3

# we run a Filter Double Rule that checks the chosen parameter
# 'INSTANCE_LENGTH_PARAM' runs against the evaluator (is this double)
# greater than our test double value (1234.567 mm = 4.050 ft)
# refer to api docs for details of the FilterDoubleRule Constructor
# http://www.revitapidocs.com/2018.1/70a53592-01d0-7d35-afbc-fb59825b4124.htm
rule = FilterDoubleRule(provider, evaluator, test, epsilon)

# generate a filter based off our Rule
filter = ElementParameterFilter(rule)

# Now we have a valid rule to run against our Filtered Element Collector.
# So in this case we pull everything inside the document
# but only if it passes our filter test
# then make sure we return the elements themselves with '.ToElements()'
analyticalCollector = fec( doc ).WherePasses( filter ).ToElements()

# To get our results back inside of Dynamo
# we need to append a list to the OUT port
OUT = analyticalCollector
