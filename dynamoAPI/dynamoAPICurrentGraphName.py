"""
DYNAMOAPI: GET CURRENT WORKSPACE NAME
"""
__author__ = 'John Pierson - sixtysecondrevit@gmail.com'
__twitter__ = '@60secondrevit'
__github__ = '@sixtysecondrevit'
__version__ = '1.0.0'
"""
Using reflection we are able to obtain the current Dynamo instance from the Revit instance.
"""
# we need to import the common language runtime to be able to interact with Dynamo & Revit

# Importing Reference Modules
# CLR ( Common Language Runtime Module )
import clr
# Adding the DynamoRevitDS.dll module to work with the Dynamo API
clr.AddReference('DynamoRevitDS')
import Dynamo 

# access to the current Dynamo instance and workspace
dynamoRevit = Dynamo.Applications.DynamoRevit()
currentWorkspace = dynamoRevit.RevitDynamoModel.CurrentWorkspace

# Access current version of dynamo
version=dynamoRevit.RevitDynamoModel.Version

# checks version of dynamo and adjusts output according to version
if version.StartsWith("1."):
	
	# Gets file name which includes full path
	filename=currentWorkspace.FileName
	
	# Splits out file path to just file name
	OUT=filename.Split("\\")[-1]

elif version.StartsWith("2."):
	OUT=currentWorkspace.Name

else:
	OUT="Not supported"
