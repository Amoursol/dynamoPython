"""
Get Package Information from a inputted file path
"""

__author__ = 'Brendan cassidy'
__twitter__ = '@brencass86'
__version__ = '1.0.0'

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

#Gets all subdirectories and files from a inputted directory
output=[["Name", "Version"]]
for root, dirs, files in os.walk(IN[0]):
	for f in files:
		if "pkg." in f:
			with open(os.path.join(root, f)) as packageFile:
				data = json.load(packageFile)
				output.append([data['name'],data['version']])

#Output
OUT= output