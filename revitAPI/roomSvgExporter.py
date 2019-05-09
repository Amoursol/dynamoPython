'''
ROOM SVG EXPORTER - EXPORT A SINGLE LEVELS ROOM BOUNDARIES
-
a dynamoPython script, visit the website for more details
https://github.com/Amoursol/dynamoPython
'''
__author__ = 'Adam Bear - adam@ukbear.com'
__twitter__ = '@adambear82'
__github__ = '@adambear82'
__version__ = '1.0.1'

'''
for large projects with lots of room data it is useful to analyse in
a business inteligence or data visualisation tool such as ms power bi.
To visualise rooms in power bi they can be cnoverted to svg and read
with the synoptic panel in power bi. This script collects rooms for a
single selected level and creates an svg file from room boundaries
'''

# -----------------------
# import modules
# -----------------------

# Common Language Runtime converts modules written in C# to python
import clr

# import built in modules
import math
import sys
from System.Collections.Generic import List
from System import DateTime
# record when svg was created so it can written into svg file
strNow = str(DateTime.Now)

# add reference for RevitAPI (Autodesk) & RevitNodes (Revit)
clr.AddReference('RevitAPI')
clr.AddReference('RevitNodes')
import Autodesk, Revit
# rather than using 'import *' import each class seperatly
# to remove conflicts with other imported classes of the same name
# notice how FilteredElementCollector is imported as fec
from Autodesk.Revit.DB import \
AreaFilter, BuiltInParameter, ElementId, ElementLevelFilter, \
ElementParameterFilter, ElementSet, ExclusionFilter, \
FilteredElementCollector as fec, \
FilterDoubleRule, FilterNumericGreater, LogicalAndFilter, \
ModelPathUtils, ParameterValueProvider, SpatialElement, \
SpatialElementBoundaryOptions, SpatialElementBoundaryLocation
# to create svg of areas instead of rooms import the room filter
# so that rooms can be filtered instead of areas
from Autodesk.Revit.DB.Architecture import RoomFilter

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
# inputs & variables
# -----------------------

# wire in a drop down level selection node to the input, and rename to
# something like 'seleect level to export room boundaries from' this
# will display the drop down in the dynamo player with this title
# which can then be used to find the name of the level
levelInput = IN[0]
levelName = levelInput.Name

# the units of room boundary curves will need to be scaled so that
# they display suitable as pixles in the svg
curveScale = 0.001

# slightly scale display of svg to improve clarity at edges
svgScale = '0.95'

# keep source code of svg neat with aligned xy values of equall length
# to convert 0.1 into +0000.100 use format specification '0=+9.3f'
# '0' specificies fill with a 0 padding character
# '=' places fill padding after the '+' sign
# '+' specifies a sign to be used on positive and negative numbers
# '9' specifies number of characters including sign ad decimal point
# '.3' specifices a precision of 3 decimal places
# 'f' specifies fixed (not floating) point to including trailing zeros
# read the docs on format specification
# https://docs.python.org/2/library/string.html#format-specification-mini-language
formatSpecification = '0=+9.3f'

# set boundary location as 'Finish' or 'Center' refer to apidocs.com
# http://www.revitapidocs.com/2018.1/349e4292-28b6-cffa-e128-50ac5c90db36.htm
boundaryLocation = 'Finish'

# set fill / stroke color of room boundaries in svg, refer to colors
# https://www.w3schools.com/colors/colors_names.asp
fillColor = 'gainsboro'
strokeColor = 'red'
# set stroke widtho froom boundaries in the svg
strokeWidth = '0.1px'

# -----------------------
# define chop
# -----------------------

# to output the numbers in the same sub list nesting as it was inputed
# clockwork provides a good example of how to chop lists unevenly
# annotated with kudos from
# https://github.com/andydandy74/ClockworkForDynamo/blob/master/nodes/1.x/List.Chop%2B.dyf


def ListChopUnevenly(chopList, chopLengths) :

	# create an empty list to return values from
	chopped = []
	# set an initail value for a counter
	count = 0
	# find the length of the list to be chopped
	max = len(chopList)

	# for each item in chopLengths
	for num in chopLengths :

		# check if counter has reached the length of the chopList
		if count + num > max :

			# set the end value as length of the chopList
			end = max

		# if counter has not reached the length of the chopList
		else :

			# set the end value as the count + num
			# eg count plus current value in chopLengths loop
			end = count + num

		# after checking above if and else conditions then
		# slice the chopList between count and end
		sliced = chopList[count:end]
		# append the sliced list to chopped
		chopped.append(sliced)
		# set the count value to end value for next loop
		count = end

	# when all loops complete return sliced list of chopped values
	return chopped

# -----------------------
# get rooms for a single level
# -----------------------

# if there are any rooms that are deleted / unplaced or otherwise
# unbounded, eg there are two rooms in a single room boundary
# they will have a room area of 0.0 and need to be filtered out
# the following filter 'filterArea0' will return rooms with an area
# greater than 0.000, eg 0.001 or greater

# built in parameter names allow us to refer to parameter names without
# having to worry about if the parameter name dispalyed in revit is in
# english, french, or another language, as it will always be the same
# refer to apidocs.com for a full list of built in parameter enumeration
# http://www.revitapidocs.com/2018.1/fb011c91-be7e-f737-28c7-3f1e1917a0e0.htm
paramArea0 = BuiltInParameter.ROOM_AREA
# provide elements to be tested by element id
providerArea0 = ParameterValueProvider(ElementId(paramArea0))
# evaulate for values greater than test value
evaluatorGr = FilterNumericGreater()
# conversion factor for square meters to square feet
sqMToSqFt = 10.7639
# because the revit API considers values in square feet we need to use
# a conversion factor to change to square meters, this is not strictly
# necessary if tested against zero, but useful to understand.
testArea0 = 0.0 * sqMToSqFt
# precision of rounding used to evaulate rule is not strictly necessary
# if tested against zero, but included so can be adapted to other values
epsilon = 10**-3
# use rule for doubles
ruleArea0 = FilterDoubleRule(
	providerArea0, evaluatorGr, testArea0, epsilon)
# filter with rule
filterArea0 = ElementParameterFilter(ruleArea0)

# adapted with kudos to archilab getRoomsByLevel
# https://gist.github.com/ksobon/8007f64a889df00afd22#file-getroomsbylevel-py

# unwrap the level selected from the dynamo node
levelUnwrapped = UnwrapElement(levelInput)
# get the Id of the level
levelUnwrappedId = levelUnwrapped.Id
# filter elements by the unwrapped level id
levelFilter = ElementLevelFilter(levelUnwrappedId)

# alias areaFilter, for areas (not rooms) we will want to exclude
areaFilter = AreaFilter()
# change to room filter if you want svg of areas not rooms
#areaFilter = RoomFilter()
# collect elements to be excluded
areaExcludes = fec(doc).WherePasses(areaFilter).ToElements()
# convert to a list if not allready so
areaExcludes = list(areaExcludes)

# create empty set and list to store elements in
element_set = ElementSet()
excludes = List[ElementId]()
# check if there are any areas to exclude
if len(areaExcludes) == 0 :
    # if there are no areas to exclude then
    # filter for levelFilter and filterArea0
    filters = LogicalAndFilter(levelFilter, filterArea0)
# otherwise if there are areas to exclude
else:
    # for each item in areaExcludes
    for i in areaExcludes:
        # use set to add items to excluded list
        element_set.Insert(i)
        elemIter = element_set.ForwardIterator()
        elemIter.Reset()
        while elemIter.MoveNext():
            curElem = elemIter.Current
            # add curent element Id in set to excluded list
            excludes.Add(curElem.Id)
    # the inverse of areaFilter
    afterExclusion = ExclusionFilter(excludes)
    # include levelFilter and afterExclusion
    filtLevExc = LogicalAndFilter(levelFilter, afterExclusion)
    # include previous filters and filterArea0
    filters = LogicalAndFilter(filtLevExc, filterArea0)

# create empty list to store room numbers in
roomNumbers = []
# collect rooms as spatial elements
# without filters this includes rooms and areas
# pass filter to exclude all areas and rooms with an area of 0.000
allRoomsOnLevel = fec(doc).OfClass(Autodesk.Revit.DB.SpatialElement)\
.WherePasses(filters).ToElements()

# for each room in all rooms on a single level
for i in allRoomsOnLevel :
    # get room number as built in parameter
    n = i.get_Parameter(BuiltInParameter.ROOM_NUMBER).AsString()
    # append room number to list
    roomNumbers.append(n)

# room numbers will be used as id when creating svg polygon

# -----------------------
# get room boundaries, scale for pixels & chop into groups
# -----------------------

# adapted with kudos to forum post by jean
# https://forum.dynamobim.com/t/bounding-box-issue/16159/9

# create an empty list to store room boundaries
roomBounds = []
# set alias for default options
opts = SpatialElementBoundaryOptions()
# string to be evaluated in loop for boundary location
bLocation = 'SpatialElementBoundaryLocation.' + boundaryLocation
# for each room in selected level
for room in allRoomsOnLevel :
    # set boundary location
    opts.SpatialElementBoundaryLocation = eval(bLocation)
    # create an empty list to store curves of room boundary
    crvs = []
    # room outer boundary is always at index [0]
    for seg in room.GetBoundarySegments(opts)[0] :
        # get the curve of the segment
        # seg.GetCurve() works for revit 2017+ for previous versions use
        # crv = seg.Curve
        # refer to piersons forum post
        # https://forum.dynamobim.com/t/lunchbox-2016-11-10-lunchbox-room-element-collector-issue/7374/4
        crv = seg.GetCurve()
        # set alias to convert curve
        convertCurve = Revit.GeometryConversion.RevitToProtoCurve
        # convert segment curve to proto geometry curve
        curve = convertCurve.ToProtoType(crv, True)
        # append converted curve
        crvs.append(curve)

    roomBounds.append(crvs)

# create empty list to store scaled curves in
scaled = []
# create empty lsit to store sub list lengthd in
boundLens = []

# for each sublist of curves in room boundaries
for i in roomBounds :
    # find the length of each sublist
    boundLen = len(i)
    # append length of curve sub list
    boundLens.append(boundLen)

    # for each curve item in sub list for each room
    for j in i :
        # scale the curve by a factor
        scaledCurve = j.Scale(curveScale)
        # find the start point of the scaled curve
        scaledPoint = scaledCurve.StartPoint
        # append the start point of the scaled curve
        scaled.append(scaledPoint)

# chop the scaled outer boundary points by the subList lengths
curveStartPoint = ListChopUnevenly(scaled, boundLens)

# -----------------------
# x & y points of curve start points
# -----------------------

# create empty lists to store values in
curveX = []
curveNY = []
curveLen = []
curveLen2 = []

for subList in curveStartPoint :
	for pt in subList :
		# round point x values to 3 places
		roundX = round(pt.X, 3)
		# append round x values
		curveX.append(roundX)
		# round point y values to 3 places
		roundY = round(pt.Y, 3)
		# multiply y value by -1 as svg rendered with y values going down
		negativeY = -1 * roundY
		# append negative y values
		curveNY.append(negativeY)
	# find length of sub list of curves to use in chop
	curveLen.append(len(subList))
	# find length of sub list of curves * 2 to use in chop later
	curveLen2.append(len(subList) * 2)

# chop the curve points by the subList lengths
choppedX = ListChopUnevenly(curveX, curveLen)
# for x and negative y
choppedNY = ListChopUnevenly(curveNY, curveLen)
# group values
choppedXNY = choppedX, choppedNY

# chopped x,-y values are used for transposing & viewBox

# -----------------------
# transpose XY values
# -----------------------

# chopped x,-y values are transposed into chooped flat pairs

# transpose values in x, -y
transposedXY = list(zip(*choppedXNY))

# pair x, -y values
pairedXY = []
for i in transposedXY :
	x = list( zip( *i ) )
	pairedXY.append(x)

flatPairs = []
# go down through 3 levels of list & sublists to find values
for i in pairedXY :
	for j in i :
		for k in j :
			# use format specification to ensure consistent
			# numbers of decimal places displayed in svg file
			formatted = format(k, formatSpecification)
			# append formatted values
			flatPairs.append(formatted)

# chop by length of sublist of curves * 2
# as values are paired chop lengths need to be doubled
choppedFlatPairs = ListChopUnevenly(flatPairs, curveLen2)
# chopped flat pairs are used later to create polygons

# -----------------------
# create polygons
# -----------------------

# create empty lists to store values in
coordslist = []
polygons = []


for xy in choppedFlatPairs :
	# join xy pairs with ',' seperator in a single list
	joinedXY = ','.join(xy)
	# append joined x, -y pairs
	coordslist.append(joinedXY)

# in coordslist and roomNumbers for each instance at the same index
for coord, num in zip(coordslist, roomNumbers) :
	# string values, including spaces, to be joined
	polygonJoins = '<polygon id=\"', num, '\" points=\"', coord, '\" />'
	# join strings with no extra spaces
	polygon = ''.join(polygonJoins)
	# append polygon values
	polygons.append(polygon)
# sort polygons
polygons.sort()
# join polygons as a single string with a new line for each item
strPolygons = '\n'.join(polygons)
# strPolygons will be used later when writing the svg file

# -----------------------
# calculate viewbox values
# -----------------------

# create a string for the svg tag with values for the view box
# all svg files start with a tag that tells browser to render as svg
svgStart = '<svg xmlns=\"http://www.w3.org/2000/svg\" \
class=\"gen-by-CTA-dyn-Synoptic-for-PowerBI\" viewBox=\"'
# the viewBox contains coords to set out where polygons are rendered
# the svg tag can include a transformation factor for scaling the svg
svgTransform = '\" transform=\"scale('
# the full string for the svg tag including the above factor and
# view box values calcualted below will be joined later in the script
svgEnd = ')\">'

# refer to x & y components of choppedXNY with simple alias
xy = choppedXNY
x = xy[0]
y = xy[1]

# min x value from nested sublist extracted using consecutive min()
xmin = min(min(x))
# min x value rounded up/down for +/-ve numbers for use in svg tag
if xmin < 0 : xminc = math.floor(xmin)
else : xminc = math.ceil(xmin)
# max x value from nested sublist extracted using consecutive max()
xmax = max(max(x))
# width of svg viewbox rounded up from, max - min
width = math.ceil(xmax - xminc)
# min y value from nested sublist extracted using consecutive min()
ymin = min(min(y))
# min y value rounded up/down for +/-ve numbers for use in svg tag
if ymin < 0 : yminc = math.floor(ymin)
else : yminc = math.ceil(ymin)
#yminc = math.ceil(ymin)
# max y value from nested sublist extracted using consecutive max()
ymax = max(max(y))
# height of svg viewbox rounded up from, max - min
height = math.ceil(ymax - yminc)
# create a list of values
svg = svgStart, xminc, yminc, width, height, svgTransform, svgScale, \
svgEnd

# create an empty list to store svg attributes in
svgAttributes = []
# for each item in svg list of values
for i in svg :
	# cast value as a string
	s = str(i)
	# join each character as a single string
	j = ''.join(s)
	# append joined strings
	svgAttributes.append(j)
# concatenate svg attributes into a single string with spaces
strOpenSvg = ' '.join(svgAttributes)

# -----------------------
# headers strings
# -----------------------

# create an ignored string to record when the svg exporter was run
strCreated = '<!--\nCreated with Chapman Taylor Dynamo SVG exporter\nby\
abear@chapmantaylor.com\n\nRevit Source File:'
# the revit file location will be added later as docFilePath
# the date will be added later as strNow
strDate = '\nDate:'
# end of the ignored string with a new line at the end
strEnd = '-->\n'
# style tag applies a style to all polygons
# stroke width controls thickness of the line
# by setting thickness a stroke can simulate a wall graphically
strOpenStyle = '\n<style>\npolygon {\nfill: '
strStroke = ';\nstroke: '
strStrokeWidth = ';\nstroke-width: '
strCloseStyle = ';\n}\n</style>'
# close the svg tag
strCloseSvg = '\n</svg>'

# list of headers to join
headersToJoin = strCreated, docFilePath, strDate, strNow, strEnd, \
strOpenSvg
# list of cascading style sheet (css) headers to join
cssPolygon = strOpenStyle, fillColor, strStroke, strokeColor, \
strStrokeWidth, strokeWidth, strCloseStyle
# join svg headers with a new line between each item in list
svgHeaders = '\n'.join(headersToJoin)
# join css headers without a new line between each item in list
cssHeaders = ''.join(cssPolygon)
# headers, polygons, and closer to svg tag
joinContent = svgHeaders, cssHeaders, '', strPolygons, strCloseSvg
# join content into a single string with new lines between items
strContent = '\n'.join(joinContent)

# -----------------------
# write svg file
# -----------------------

# the svg just needs to be written to a file now

# save the svg to the same folder as the revit file
# include the level name in the svg file name
svgPath = docPathFolder + levelName + ' - rooms.svg'
# use try to allow a message to be displayed if fails
try :
	# use with so that file does not need to be manually closed
	with open(svgPath, 'w') as file :
		# write the svg file
		file.write(strContent)
		# display a message with the svg path on a new line
		svgMsg = 'svg updated' + '\n' + svgPath
# if the file write fails
except :
	# display a fail message
	svgMsg = 'svg not updated'

# the svg file has been created

# -----------------------
# out
# -----------------------

# send the svgMsg to the OUT port
OUT = svgMsg
