'''
ROOM DATASHEET EXPORTER - EXPORT RDS CSV
-
a dynamoPython script, visit the website for more details
https://github.com/Amoursol/dynamoPython
'''
__author__ = 'Adam Bear - adam@ukbear.com'
__twitter__ = '@adambear82'
__github__ = '@adambear82'
__version__ = '1.0.0'

'''
for large projects with lots of room data it is useful to analyse in
a business inteligence or data visualisation tool such as ms power bi.
This data could be simply exported from revit as a room schedule,
however for a single power bi template to work for many projects across
a practice the room data needs to be formatted in a consistent way that
would be subject to user error. This script exports a csv file of room
data. The user can define what parameters to use which can easily be
changed in dynamo player.
'''

# -----------------------
# import modules
# -----------------------

# Common Language Runtime converts modules written in C# to python
import clr

# add reference for RevitAPI (Autodesk) so we can use the API
clr.AddReference('RevitAPI')
import Autodesk
# rather than using 'import *' import each class seperatly
# to remove conflicts with other imported classes of the same name
# notice how FilteredElementCollector is imported as fec
from Autodesk.Revit.DB import BuiltInCategory, \
FilteredElementCollector as fec

# add reference for RevitServices (RevitServices)
clr.AddReference('RevitServices')
import RevitServices
# Import DocumentManager
from RevitServices.Persistence import DocumentManager
# use alias for document manager for ease of reference
doc = DocumentManager.Instance.CurrentDBDocument
# file path and file name of the current revit document
docFilePath = doc.PathName
# remove file name as string after final '\' character in file path name
docPath = docFilePath.rsplit('\\', 1)[0]
# add '\' to end of string for folder path name
docPathFolder = docPath + '\\'

# -----------------------
# define chop
# -----------------------


# to output the numbers in the same sub list nesting as it was inputed
# clockwork provides a good example of how to chop lists evenly
# https://github.com/andydandy74/ClockworkForDynamo/blob/master/nodes/1.x/List.Chop+.dyf
def ListChopEvenly(l, n):
	# Andreas provides reference from stack overflow with python 2 example
	# https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
	return [l[i:i + n] for i in xrange(0, len(l), n)]

# -----------------------
# input parameters
# -----------------------

# in the dynamo environment wire a string node to the input
# rename the string node to something like 'room parameters to export to
# csv' and enter some default values like 'Number, Name, Area'
# when run in dynamo player this will give the user the ability to enter
# their own values for the string
inputParams = IN[0]
# some people might use a space, some people might not, others might
# enter in double spaces. so split can be used consistently,
# we remove any spaces replacing them with a zero length string
replaceParams = inputParams.replace(' ', '')
# so we can use each item in the user entered string seperatelt
# we need split the string into list using the comma, seperator
params = replaceParams.split(',')
# so we can chop a flat list into groups we need to know its lengths
paramsLen = len(params)

# -----------------------
# parameter values
# -----------------------

# collect all rooms as elements
allRooms = fec(doc).OfCategory(BuiltInCategory.OST_Rooms).ToElements()
# we will need somehere to store values for csv
values = []
# to lookup the parameter value, for each parameter, for each room
for r in allRooms :
	for p in params :
		value = r.LookupParameter(p)
		# depending on if the parameter value is a string or a double
		# we will need to handle it differently, so its important to
		# find the storage type of the parameter value
		strStorageType = value.StorageType.ToString()

		# if storage type is a string
		if strStorageType == 'String' :
			# cast value as string
			strValue = value.AsString()
			# append values
			values.append(strValue)

		# if storage type is a double
		elif strStorageType == 'Double' :
			# cast value as double
			doubleValue = value.AsDouble()
			# convert square feet to square meters for area
			if p == "Area" :
				doubleValue = doubleValue * 0.092903 
			# round the double value
			doubleRound = round(doubleValue, 3)
			# append values
			values.append(doubleRound)

# a flat list values needs to be chopped into groups by list length
choppedValues = ListChopEvenly(values, paramsLen)
choppedValues.sort()

# the csv will need to have as headers for each parameter
headers = []
for p in params :
	headers.append(p)
choppedValues.insert(0, headers)

# -----------------------
# write csv file of room parameters
# -----------------------

# create empty list to store values
rowCsvValue = []
# for each chopped value
for i in choppedValues :
	# remove first and last characters '[' , ']'
	csvItem = str(i)[1:-1]
	# append values
	rowCsvValue.append(csvItem)
# join each row as a new line in a single string
csvValues0 = '\n'.join(rowCsvValue)
# remove backslash characters '\'
csvValues = csvValues0.replace('\'', '')

# there are a number of reasons why trying to write a csv file
# might fail, for example the file might be allready be open,
# by using the try statement we can catch the failure and adjust the
# code to suite
try :
	# use with to automate closing of file when loop finished
	with open(docPathFolder + 'rooms.csv', 'w') as file :
		# write csv with values
		file.write(csvValues)
		# set help message to show location of csv
		csvMsg = 'csv updated' + '\n' + docPathFolder + 'rooms.csv'
# set help message if file write fails
except :
	csvMsg = 'csv not updated'

# -----------------------
# out
# -----------------------

# send the csvMsg to the OUT port, in the dynamo enviroment wire a
# watch node and rename it to something like 'csv message' this will
# show the contents of the watch node in dynamo player with the title
# of the renamed watch node
OUT = csvMsg
