"""
Get Package Information from a inputted file path
"""

__author__ = 'Brendan cassidy'
__twitter__ = '@brencass86'
__version__ = '1.0.1'

import clr

#Sets up new path to ironpython module Library
#See https://docs.python.org/2/library/sys.html
import sys
sys.path.append("C:\Program Files (x86)\IronPython 2.7\Lib")

#Imports operating system interfaces
#See https://docs.python.org/2/library/os.html
import os

#Imports Json module
import json

def GetPackageInfo(input):
	output=[["Host Application", "Dynamo Version", "Package Name", "Package Version"]]

	for root, dirs, files in os.walk(input):
		for f in files:
			if "pkg." in f:
				with open(os.path.join(root, f)) as packageFile:
					data = json.load(packageFile)
					output.append([GetApplication(input),GetVersion(input),data['name'],data['version']])
	return zip(*output)

def GetVersion(input):
	templist=input.split('\\')
	listcount=len(templist) 
	
	return templist[listcount-2]

def GetApplication(input):
	if "Revit" in input:
		return "Revit"
	elif "Civil" in input:
		return "Civils 3D"
	else:
		return "NA"


if IN[0]:
	OUT="Current",GetPackageInfo(IN[1][0])
else:
	output,sheetName=[],["Current"]
	count = 0
	for a in IN[1][1]:
		sheetName.append(GetVersion(a))
		output.append(GetPackageInfo(a))
	OUT=sheetName,[GetPackageInfo(IN[1][0])] + output
