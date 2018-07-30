'''
COLOR BY GROUP - VISUALISE GROUPS AS IN GROUP BY KEY
'''
__author__ = 'Adam Bear - adam@ukbear.com'
__twitter__ = '@adambear82'
__version__ = '1.0.0'

# IMPORTS / REFERENCES:
import clr
clr.AddReference('DSCoreNodes')
import DSCore
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *
clr.AddReference('Display')
from Display import *

# IN PORTS:
geometry = IN[0]

# define all the colors of the rainbow in a spectrum list
c00 = red = DSCore.Color.ByARGB(255, 255, 000, 000)
c02 = yellow = DSCore.Color.ByARGB(255, 255, 255, 000)
c04 = green = DSCore.Color.ByARGB(255, 000, 255, 000)
c06 = cyan = DSCore.Color.ByARGB(255, 000, 255, 255)
c08 = blue = DSCore.Color.ByARGB(255, 000, 000, 255)
c10 = magenta = DSCore.Color.ByARGB(255, 255, 000, 255)
spectrum = c00, c02, c04, c06, c08, c10

# similar to color range node indicies need to be mapped to each color
# red (0.0), yellow(0.2), green(0.4), cyan(0.6), blue(0.8), magenta(1.0)
# if we assumed the spectrum values did not change this could simply be
# sU = sV = 0.0, 0.2, 0.4, 0.6, 0.8, 1.0
# in designscript we would use the following
# 0..1..#List.Count(spectrum)
# for a rigorous approach lets look at how to acheive this in python
# for all the values in the range of the length of spectrum
# each value is multipled by the inverse of the length of the spectrum-1
# if we did not -1 then the factor would be (1/6=0.16) not (1/5=0.20)
# for more info refer to
# https://github.com/Amoursol/dynamoPython/blob/master/concepts/numberSequences.py
sU = [ value * 1.0 / (len(spectrum) - 1) for value in range( len(spectrum) ) ]
# although the spectrum UV is 2D by stating sU=sV the color range is 1D
# for more complex requirements a different set of values could be given
sV = sU

# create the empty list sUV to hold UV coordinates of the spectrum
sUV = []
# for every item in lists sU and sV
# append to sUV the result of UV.ByCordinates
for u, v in zip(sU, sV) :
	sUV.append(UV.ByCoordinates(u, v))

# the color range of the spectrum is mapped to indices using UV coords
colorrange2d = DSCore.ColorRange2D.ByColorsAndParameters(spectrum, sUV)

# as above for spectrum UVs, geometry UVs are listed
# in design script this would be
# 0..1..#List.Count(geometry)
# because the geometry is variable we must calculate this list
gU = [ value * 1.0 / (len(geometry) - 1) for value in range( len(geometry) ) ]
# although the geometry UV is 2D by stating gU = gV the mapping is 1D
# for more complex requirements a different set of values could be given
gV = gU

# create the empty list gUV to hold UV coordinates of the geometry
gUV = []
# the color range of the geometry is mapped to values using UV coords
for u, v in zip(gU, gV) :
	gUV.append(UV.ByCoordinates(u, v))

# create an empty list colors to hold values of colors to be displayed
colors = []
# for each item in the geometry UV
for i in gUV :
	# append the coresponding spectrum UV
	colors.append(colorrange2d.GetColorAtParameter(i))

# create an empty list colorByGroup to hold geometry displayed in color
colorByGroup = []
# for each item 'geom' in the geometry
for geom, c in zip(geometry, colors) :
	for g in geom :
		colorByGroup.append(Display.ByGeometryColor(g, c))


# to output the displayed geometry in the same groups as it is inputed
# clockwork provides a good example of how to chop lists evenly
# https://github.com/andydandy74/ClockworkForDynamo/blob/master/nodes/1.x/List.Chop+.dyf
def ListChopEvenly(l, n):
	# Andreas provides reference from stack overflow with python 2 example
	# https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
	return [l[i:i + n] for i in xrange(0, len(l), n)]
# clockworks chop definition is used to chop the geometry
choppedGroups = ListChopEvenly(colorByGroup, len(geometry))

# the choppedGroups are sent to the OUT port
OUT = choppedGroups
