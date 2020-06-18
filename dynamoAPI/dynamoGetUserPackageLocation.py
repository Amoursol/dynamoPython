"""
DYNAMOAPI: Get User Package Location For Currently Running Dynamo Application
"""

__author__ = 'Brendan cassidy'
__twitter__ = '@brencass86'
__version__ = '1.0.0'

"""
This will gather the correct user package location depending on what version of dynamo is running in either Civil 3d or Revit. 
Then it will output a path to the currently running user appdata folder for dynamo
"""

import clr

# Sets up new path to ironpython module Library
# See https://docs.python.org/2/library/sys.html
import sys
sys.path.append("C:\Program Files (x86)\IronPython 2.7\Lib")

# Imports operating system interfaces
# See https://docs.python.org/2/library/os.html
import os

# Module to read a dll assembly version
from System.Diagnostics import FileVersionInfo

# Function to trim string version input down to main version
def GetReducedVersion(input):
	# Strings version down to main version
	count=0
	stringIndex=[]
	for a in input:
		if a == ".":
			stringIndex.append(count)
		count=count+1
	return input[0:stringIndex[1]]

# Trys to find Revit API, if it errors out it will skip
try:
	# Import DocumentManager
	clr.AddReference("RevitServices")
	import RevitServices
	from RevitServices.Persistence import DocumentManager
	
	# Import RevitAPI
	clr.AddReference("RevitAPI")
	import Autodesk
	from Autodesk.Revit.DB import *
	
	# Standard areas for Current Document, Active UI and application
	uiapp = DocumentManager.Instance.CurrentUIApplication
	app = uiapp.Application
	
	# Gets current Revit Version
	revitVersion = int(app.VersionNumber)
	
	# Only runs if revit version is higher than 2019
	if revitVersion > 2019:
		
		# Constructs path depending on revit version this is run from
		FolderLocation = 'C:\\Program Files\\Autodesk\\Revit ' + app.VersionNumber +  '\\AddIns\\DynamoForRevit\\'
		
		# Gets Dynamo Core dll file Version
		DynamoCoreVersion = FileVersionInfo.GetVersionInfo(FolderLocation + "DynamoCore.dll").FileVersion
		
	# Uses a different method to get dynamo core version if not in revit 2020 or higher
	else:
		clr.AddReference('DynamoRevitDS')
		import Dynamo 
		
		# access to the current Dynamo instance and workspace
		dynamoRevit = Dynamo.Applications.DynamoRevit()
		currentWorkspace = dynamoRevit.RevitDynamoModel.CurrentWorkspace
		
		# Access current version of dynamo
		DynamoCoreVersion=dynamoRevit.RevitDynamoModel.Version
		
	# Constructs the user package location path	
	OUT = os.getenv('APPDATA') + '\\Dynamo\\Dynamo Revit\\' + GetReducedVersion(DynamoCoreVersion) + '\\packages'
		
# outputs a error to do something else if it cannot find Revit API
except:
	# Trys to find Autocad API, if it errors out it will skip
	try:
		# Add Assemblies for AutoCAD and Civil3D
		clr.AddReference('AcMgd')
		clr.AddReference('AcCoreMgd')
		clr.AddReference('AcDbMgd')
		
		import Autodesk.AutoCAD.ApplicationServices.Application as acapp
				
		# What the Versions means to year version
		#  https://knowledge.autodesk.com/support/autocad/learn-explore/caas/CloudHelp/cloudhelp/2021/ENU/AutoCAD-Core/files/GUID-793238B6-F8B8-4D20-BB3A-001700AECD75-htm.html
		appBuildVersion = float(acapp.Version.Major.ToString() + "." + acapp.Version.Minor.ToString())
		
		# Gets Autocad Build version then transfer it to year version
		if appBuildVersion == 23.1:
			appVersion = "2020"
		elif appBuildVersion == 24.0:
			appVersion = "2021"
		else:
			appVersion = "NA"
		
		# If AppVersion is NA eg not civil 3d versions 2020 or 2021 then output not supported
		if appVersion == "NA":
			OUT = "This code does not support Civil 3D 2019 or less"
		
		# Goes to correct folder location of DynamoCore and checks its version	
		else:
			dynamoCoreLoc = 'C:\\Program Files\\Autodesk\\AutoCAD ' + appVersion + '\\C3D\Dynamo\\Core\\DynamoCore.dll'
		
			# Gets Dynamo Core dll file Version
			DynamoCoreVersion = FileVersionInfo.GetVersionInfo(dynamoCoreLoc).FileVersion

			# Constructs the user package location path
			OUT = os.getenv('APPDATA') + '\\Autodesk\C3D ' + appVersion + '\\Dynamo\\' + GetReducedVersion(DynamoCoreVersion) + '\\packages'
	
	# Outputs a error that this wasnt run from within a dynamo hosted in revit or Civil 3D
	except:	
		OUT = "This code only works within revit/Civils 3d"
