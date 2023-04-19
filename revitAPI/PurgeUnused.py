'''
This will purge out all elements it can from the current project file.
Note: 
	This code will only work in revit 2024 and above because of the new Revit api
	This Python code is based of IronPython2 python engine
'''
__author__ = 'Brendan cassidy'
__twitter__ = '@brencass86'
__version__ = '1.0.0'

import clr

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

# Imports HashSet from System.
clr.AddReference("System.Core")
from System.Collections.Generic import HashSet


# Standard areas for Current Document, Active UI and application
doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication

# Gets revit version number
rvtVersion = uiapp.Application.VersionNumber

# Creates a new hastset that is
catIdList = HashSet[ElementId]()

# items used to aid run count and total amount of elements deleted
purgeCount = 0
delTotal = 0

# Checks and makes sure it will only run in revit 2024 and above.
if rvtVersion >= 2024:
	
	# Checks the purge count is not over 10 
	while purgeCount < 10:
		
		# Extracts Unsured Elements from a list of categories
		# List is empty and therefore it will get all unused item in project file
		purgeElements = doc.GetUnusedElements(catIdList)
		
		# Checks that there are items to be purged
		if purgeElements.Count > 0:	
			# Starts a transaction and then deletes the unused elements
			TransactionManager.Instance.EnsureInTransaction(doc)
			doc.Delete(purgeElements)
			TransactionManager.Instance.TransactionTaskDone()
			
			# Totals up the amount of items deleted
			delTotal = delTotal + purgeElements.Count
		
		# Breaks out if there is no elements to purge
		else:
			break
		# Add a 1 to the purgecount for use within the while statement
		purgeCount += 1
	
	# Adjusts output depending on if there are items deleted
	if delTotal == 0:
		OUT = "There was no Elements to purge out of the current opened file."
	else:
		# Outputs the amount of elements that was deleted and how many times the delete/purge command was run.
		OUT = "Purge Elements Ran a total of " + purgeCount.ToString() + " times \n and deleted " + delTotal.ToString() + " elements."

# Indicates if the revit version is lower than Revit 2024.
else:
	OUT = "Your version of Revit is lower than the minimum of Revit 2024."
