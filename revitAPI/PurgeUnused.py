'''
This will purge out all elements it can from the current project file.
Note: 
	This code will only work in revit 2020 and above. In revit 2024 it will 
 	utilise the new Revit api, and in 2020 to 2023 it will utilise eTransmit.
	This Python code is based of IronPython2 python engine
'''
__author__ = 'Brendan cassidy'
__twitter__ = '@brencass86'
__version__ = '2.0.0'

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
rvtVersion = int(uiapp.Application.VersionNumber)

# Checks for Revit 2024 because Native get unused api was released in this version.
if rvtVersion >= 2024:

	# Starts of the counts/totals at 0.
	purgeCount = 0
	delTotal = 0
	
	# Creates a new hastset of ElementID's
	catIdList = HashSet[ElementId]()
	
	# Checks the purge count is not over 10 
	while purgeCount < 10:
		
		# Extracts Unsused Elements from a list of categories, though this list is empty and
		# therefore it will get all unused item in project file. More info on the api can be found on RevitAPi docs 
		# or https://thebuildingcoder.typepad.com/blog/2023/04/whats-new-in-the-revit-2024-api.html#4.2.15
		purgeElements = doc.GetUnusedElements(catIdList)
		
		# Checks that there are items to be purged
		if purgeElements.Count > 0:	
			# Starts a transaction and then deletes the unused elements
			TransactionManager.Instance.EnsureInTransaction(doc)
			doc.Delete(purgeElements)
			TransactionManager.Instance.TransactionTaskDone()
			
			# Totals up the amount of items deleted
			delTotal = delTotal + purgeElements.Count
		
		# Breaks out if there are no elements to purge
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

# Checks for revit 2020 to 2023 as this utilises the Etranmit API which has a Purge unused.
elif 2020 <= rvtVersion <= 2023:
	# Loads in the correct version of Etransmit dll's
	if rvtVersion == 2020:
		sys.path.append(r'C:\Program Files\Autodesk\eTransmit for Revit 2020')
	elif rvtVersion == 2021:
		sys.path.append(r'C:\Program Files\Autodesk\eTransmit for Revit 2021')
	elif rvtVersion == 2022:
		sys.path.append(r'C:\Program Files\Autodesk\eTransmit for Revit 2022')
	elif rvtVersion == 2023:
		sys.path.append(r'C:\Program Files\Autodesk\eTransmit for Revit 2023')
	
	#Imports the eTransmit 
	clr.AddReference("eTransmitForRevitDB")
	import eTransmitForRevitDB as eTransmit
	
	# does the purge unused at least 5 times to make sure all is purged
	for i in range(5):
		eTransmitUpgradeOMatic = eTransmit.eTransmitUpgradeOMatic(app)
		resultPurg = eTransmitUpgradeOMatic.purgeUnused(doc)

	OUT =  doc.Title + " has been purged. "

# Indicates it cannot be used on revit 2019 or earlier.
else:
	OUT = "Your current version of revit is unsupported"
