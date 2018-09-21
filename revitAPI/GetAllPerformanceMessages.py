'''
GET ALL POSSIBLE PERFORMANCE MESSAGES
'''
__author__ = 'Brendan cassidy'
__twitter__ = '@brencass86'
__github__ = 'Brencass'
__version__ = '1.0.0'

# import common language runtime 
import clr

# Import RevitAPI
clr.AddReference("RevitAPI")
# import all classes from Revit DB
from Autodesk.Revit.DB import *

# Gets access to performance adviser object
adviser = PerformanceAdviser.GetPerformanceAdviser()

# Access to all rules
ruleids = adviser.GetAllRuleIds()

# Declares a list 
adviserName = []
adviserDescription=[]

# iterate through the performance advisers and append Name/description to output
for ri in ruleids:
	adviserName.append(adviser.GetRuleName(ri))
	adviserDescription.append(adviser.GetRuleDescription(ri))

# return the results
OUT = [adviserName,adviserDescription]
