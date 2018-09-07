'''
CLASH SVG EXPORTER - EXPORT NAVISWORKS CLASHES FROM XML TO SVG
-
a dynamoPython script, visit the website for more details
https://github.com/Amoursol/dynamoPython
'''
__author__ = 'Adam Bear - adam@ukbear.com'
__twitter__ = '@adambear82'
__github__ = '@adambear82'
__version__ = '1.0.0'

'''
for large projects with lots of clash data it is useful to analyse in
a business inteligence or data visualisation tool such as ms power bi.
exporting clashes from navisworks to an xml file provides a useful
format to extract data from. Ensure clashpoint and distance are
exported to the xml report, otherwise index lookups in code will need
to be adjusted. This script exports a svg file of circles at points
here clashes occur, and polygons where room boundaries are found to
give a context.
'''

# -----------------------
# import modules
# -----------------------

# Common Language Runtime converts modules written in C# to python
import clr
# import built in modules
import math
# to import modules we need to use sys
import sys
# now we can define where to look for a library of useful moduels
pythonPath = 'C:\\Program Files (x86)\\IronPython 2.7\\Lib'
# appending pythonPath to sys path allow us to import modules from there
sys.path.append(pythonPath)
# lets import element tree and for ease refer to it as et
import xml.etree.ElementTree as et
# so we can record when svg was created create astring of current time
from System import DateTime
strNow = str(DateTime.Now)
# to use List[ElementId]() in archilab getRoomsByLevel
from System.Collections.Generic import List

# add reference for RevitAPI (Autodesk) & RevitNodes (Revit)
clr.AddReference('RevitAPI')
clr.AddReference('RevitNodes')
import Autodesk, Revit
# rather than using 'import *' import each class seperatly
# to remove conflicts with other imported classes of the same name
# notice how FilteredElementCollector is imported as fec
from Autodesk.Revit.DB import \
AreaFilter, BasePoint, BuiltInParameter, ElementId, ElementLevelFilter,\
ElementParameterFilter, ElementSet, ExclusionFilter, \
FilteredElementCollector as fec, \
FilterDoubleRule, FilterNumericGreater, LogicalAndFilter, \
ModelPathUtils, ParameterValueProvider, SpatialElement, \
SpatialElementBoundaryOptions, SpatialElementBoundaryLocation, XYZ

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
# inputs
# -----------------------

# wire in a file path node and browse to xml report exported from
# navisworks, ensure report includes clash point and distance,
# if distance is not included indexs used later in script will need to
# be adjusted to suit
xmlClashes = IN[0]
# the imported module element tree parses the xml file so we can
# look at the data inside the xml
tree = et.parse(xmlClashes)
# the file name is the last part of the file path without its extension
xmlFileName = xmlClashes.split('\\')[-1].split('.xml')[0]

# wire in a drop down level selection node to the input, and rename to
# something like 'seleect level to export room boundaries from' this
# will display the drop down in the dynamo player with this title
levelInput = IN[1]
# we can find the name of the level easily
levelName = levelInput.Name

# -----------------------
# variables
# -----------------------

# xps is shorthand for X Path String
# the full string can be shortened to the last tag if unique
# './/batchtest/clashtests/clashtest/clashresults/clashresult'
xps_clashresult = './/clashresult'
# './/batchtest/clashtests/clashtest/clashresults/clashresult/clashpoint/pos3f'
xps_pos3f = './/pos3f'

# slightly scale display of svg to improve clarity at edges
svgScale = '0.99'
# add a padding value so that viewbox does not clip edges of circles
pad = 5

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
# set fill / stroke color of room boundaries in svg, refer to colors
# https://www.w3schools.com/colors/colors_names.asp
circleFill = 'none' # 'gainsboro'
circleStroke = 'red'
# stroke width controls thickness of clashes in the svg
circleWidth = '0.1'
# set the radius of the circle
circleRadius = '0.5'

# the units of room boundary curves will need to be scaled so that
# they display suitable as pixles in the svg
curveScale = 0.001

# set boundary location as 'Finish' or 'Center' refer to apidocs.com
# http://www.revitapidocs.com/2018.1/349e4292-28b6-cffa-e128-50ac5c90db36.htm
boundaryLocation = 'Finish'

# set fill / stroke color of room boundaries in svg, refer to colors
# https://www.w3schools.com/colors/colors_names.asp
polyFill = 'cornsilk'
polyStroke = 'red'
# set stroke width froom boundaries in the svg
# by setting thickness a stroke can simulate a wall graphically
polyWidth = '0.1px'
# set a transition speed on mouse over polygon rooms
polyTrans = '500ms'
# set a color for polygon rooms on mouse over
polyHover = 'pink'

# -----------------------
# define functions
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


# to find attribute values of xml tag
# simplified and annotated with kudos to bakery node
# XPATH Expression Find for Element Tree.dyf
# https://github.com/LukeyJohnson/BakeryForDynamo/blob/97e5622db7ba14cd42caac9b8bd4fdba6b66871e/nodes/XPATH%20Expression%20Find%20for%20Element%20Tree.dyf
def xmlAttrib(tree, xPathStr) :

	root = tree.getroot()
	xpathfound = root.findall(xPathStr)
	xtags, xcountattrib, xattrib, xattvals = [], [], [], []
	# when trying to use xpath.attrib with element tree we get the error
	# 'string' does not contain a definition for 'Key'
	# this is a known issue in dynamo and is tracked here
	# https://github.com/DynamoDS/Dynamo/issues/3100
	# bakery method side steps this by finding names and values of keys
	for x in xpathfound:
		if x.keys():
			xcountattrib.append(len(x.items()))
			for name, value in x.items():
				xattrib.append(name)
				xattvals.append(value)
		# if there is not a key then the counter is increased
		else:
			xcountattrib.append(1)
			xattvals.append('_none_')

	# here we nest chop to return values neatly chopped & transposed
	chopped = ListChopUnevenly(xattvals, xcountattrib)
	transposed = list(zip(*chopped))
	return transposed

# -----------------------
# get project base point adjustments to survey point
# -----------------------

# cant remember where this script comes from but kudos all the same
# https://forum.dynamobim.com/t/converting-from-model-coordinates-to-shared-coordinates/21411/2
# api returns values in feet and need to be converted into mm
ft2mm = 304.8

# assume the adjustment should be realtive to 0,0,0
# get the project base point relative to 0,0,0
origin = XYZ(0.0, 0.0, 0.0)
projLoc = doc.ActiveProjectLocation
projPos = projLoc.get_ProjectPosition(origin)

# get the east west and north south project positions
# convert from feet to mm and round to 6 decimal places
outProjLoc = []
outProjLoc.append(round(projPos.EastWest * ft2mm, 6))
outProjLoc.append(round(projPos.NorthSouth * ft2mm, 6))

# define values for adjusting project base point to survey point
# change the units from mm to m
pbpAdjust = outProjLoc
pbpAdjustX = round(projPos.EastWest * ft2mm, 6) / 1000
pbpAdjustY = round(projPos.NorthSouth * ft2mm, 6) / 1000

# projectLocationData = outProjLoc, outProjBasePt, outProjSurvPt

# -----------------------
# get attributes from xml file
# -----------------------

# clashtest_attrib = xmlAttrib(tree, xps_clashtest)

# navisworks exports an xml of clashes with the tag clashresult for
# each clash, this includes the attributes for clash distance, name and
# guid. Unfortunately dynamo's implementaion of python does not allow us
# to use the attrib property with element tree, luckily bakery has a
# work around which we can use as a function below
clashresult_attrib = xmlAttrib(tree, xps_clashresult)
# most clash xml exports are likely to always include distance
# however if the distance is not exported from navisworks to xml
# then the indices need to be moved up to 0 and 1
# clashresult_distance = clashresult_attrib[0]
clashresult_name = clashresult_attrib[1]
clashresult_guid = clashresult_attrib[2]

# -----------------------
# concatenate test clash
# -----------------------

# the circles in the svg need an id so that they can be selected in
# power bi. Simply using the name of the clash would work if only a
# single clash test was exported to xml. however for xml reports that
# contain multiple tests there will need to be a way of differentiating
# between clash1 in clashTestA and clash1 in ClashTestB

"""
# creating an id for each clash in the format 'testName_clashNumber'
# is possible in python as below, currently this is not useable in
# ms power bi, but this may be improved in the future so is kept for
# future reference, in any case it is a good excercise

clashtests = tree.findall('.//clashtest')
testnamevalue = []
for clashtest in clashtests :
	if clashtest.keys() :
		for name, value in clashtest.items() :
			if name == 'name' :
				testnamevalue.append(value)

lenTests = []
for clashtest in clashtests :
	lenTest = 0
	for clashresults in clashtest :
		if clashresults.tag == 'clashresults' :
			for clashresult in clashresults :
				if clashresult.tag == 'clashresult' :
					lenTest += 1
			lenTests.append(lenTest)

clashresult_attrib = xmlAttrib(tree, xps_clashresult)
clashresult_name = clashresult_attrib[1]

groupedTests = []
for t,l in zip(testnamevalue, lenTests) :
	test = [t] * l
	groupedTests.append(test)

tests = []
for sublist in groupedTests :
	for t in sublist :
		tests.append(t)

clashresult_testName = []
for t,n in zip (tests,clashresult_name) :
	testName = t + '_' + n
	clashresult_testName.append(testName)
"""

# although less readable in the svg file, a simpler method of creating
# unique clash ids is use the format 'clashNumber_clashGuid'

# we will need somewhere to store svg circle ids
clashresult_nameGuid = []
for n, g in zip(clashresult_name, clashresult_guid) :
	# append a string of the name_guid to ensure value is unique
	clashresult_nameGuid.append(n + '_' + g)

# navisworks exports an xml of clashes with the tag pos3f for each clash
# this includes attributes for x, y, z values of the clashes position.
# again we use the bakery function to find attributes for each clash
pos3f_attrib = xmlAttrib(tree, xps_pos3f)
# we dont really need the z value as a svg is 2d only
# pos3f_zPositive = pos3f_attrib[0]
pos3f_yPositive = pos3f_attrib[1]
pos3f_xPositive = pos3f_attrib[2]

# the circles in the svg need an x and y coordinate so they can be
# positioned in the svg. values need to be converted from strings to
# doubles so we can do some math with them later to find the viewbox
# of the svg
pos3f_x = []
for x in pos3f_xPositive :
	floated = float(x)
	# revit api will report boundaries relative to project base point
	# navisworks reports clash points relative to survey point so that
	# revit room boundaries and navisworks clash points can be overlaid
	# adjust navisworks xy coordinates for project base point difference
    # to survey point
	pbpAdjustedX = floated - pbpAdjustX
	pos3f_x.append(pbpAdjustedX)

# the y coordinate needs to be multiplied by -1.0 as svgs are drawn from
# the top down, because they are usually used in web browsers, whereas
# revit draws from the bottom up
pos3f_y = []
for y in pos3f_yPositive :
	pos3f_yNegative = -1.0 * float(y)
	# adjust navisworks xy coordinates for bpb difference to sp
	pbpAdjustedY = pos3f_yNegative + pbpAdjustY
	pos3f_y.append(pbpAdjustedY)

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

# min x & y values rounded up for use in svg tag
xminc = (min(pos3f_x))
yminc = (min(pos3f_y))
# width & height of svg viewbox rounded up from, max - min
width = math.ceil(max(pos3f_x) - min(pos3f_x))
height = math.ceil(max(pos3f_y) - min(pos3f_y))
# so that the svg does not touch the edge of the web browser
# define a value for padding and adjust values to suite
xminc = xminc - (pad / 2)
yminc = yminc - (pad / 2)
width = width + pad
height = height + pad

# create a list of values
svg = svgStart, xminc , yminc, width, height, \
svgTransform, svgScale, svgEnd

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
# circles for clashes
# -----------------------

circles = []
for x, y, id in zip(pos3f_x, pos3f_y, clashresult_nameGuid) :
	# format the strings using format specification so all
	# values align neatly in the svg file
	x = format(x, formatSpecification)
	y = format(y, formatSpecification)
	# define valuesto be used for each circle
	circleValues = '<circle id=\"', id, '\" cx=\"', str(x), '\" cy=\"',\
	str(y), '\" r=\"', circleRadius, '\" />'
	# append the joined valeus for each clash as a list of strings
	joinedCircles = ''.join(circleValues)
	circles.append(joinedCircles)
# create a single string of all values with new lines for each circle
strCircles = '\n'.join(circles)

# http://patorjk.com/software/taag/#p=display&f=Small%20Slant&t=kudos
# -----------------------
#                __                  
#     ___  ___  / /_ _____ ____  ___ 
#    / _ \/ _ \/ / // / _ `/ _ \/ _ \
#   / .__/\___/_/\_, /\_, /\___/_//_/
#  /_/          /___//___/           
#
# -----------------------
# polygons - get rooms for a single level
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
# polygons - get room boundaries, scale for pixels & chop into groups
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
# polygons - x & y points of curve start points
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
#    ____  _____ _
#   (_-< |/ / _ `/
#  /___/___/\_, / 
#          /___/  
#
# -----------------------
# headers strings
# -----------------------

# join svg headers with a new line between each item in list
svgHeaders = '\n'.join((
'<!--\nCreated with Chapman Taylor Dynamo SVG exporter',
'by abear@chapmantaylor.com',
'',
'xml clash report source file:',
docFilePath,
'',
'Date:',
strNow,
'-->\n'
))

# circles can be controlled using variables at the top of the script
cssCircle = ''.join((
'circle {\n',
'fill: ', circleFill, ';\n',
'stroke: ', circleStroke, ';\n',
'stroke-width: ', circleWidth, ';\n',
'}'
))

# polygons are styled as
cssPolygon = ''.join((
'polygon {\n',
'fill: ', polyFill, ';\n',
'stroke:', polyStroke, ';\n',
'stroke-width: ', polyWidth, ';\n',
'}'
))

# when hovering over polygons they are styled as
cssPolygonHover = ''.join((
'polygon:hover {\n',
'transition: ', polyTrans, ';\n',
'fill:', polyHover, ';\n',
'}'
))

# join css headers without a new line between each item in list
cssStyles = '\n'.join((
'<style>', cssCircle, cssPolygon, cssPolygonHover, '</style>'
))

# join content into a single string with new lines between items
strContent = '\n'.join((
svgHeaders, strOpenSvg, '', cssStyles, '', strPolygons, '',
strCircles, '', '</svg>'
))

# -----------------------
# write svg file
# -----------------------

# the svg just needs to be written to a file now

# save the svg to the same folder as the revit file
# include the level name in the svg file name
svgPath = docPathFolder + xmlFileName + ' - clashtest.svg'
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
