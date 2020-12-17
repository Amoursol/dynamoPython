"""
xMasTree - Joke
-
a dynamoPython script, visit the website for more details
https://github.com/Amoursol/dynamoPython
"""

__author__ = 'Adam Bear - adam@ukbear.com'
__twitter__ = '@adambear82'
__github__ = '@adambear82'
__version__ = '1.0.0'

"""
just for fun at xMas heres an xMas tree, a yMas tree and a zMas tree !
"""

import clr # common runtime library allows us to add references

clr.AddReference('ProtoGeometry') # were going to use a cone for the tree
from Autodesk.DesignScript.Geometry import Cone, Geometry, Point, Plane

clr.AddReference('GeometryColor') # were going to recolor xyz cones
from Modifiers import GeometryColor

clr.AddReference('DSCoreNodes')
import DSCore # enable design script in python

ptStart		= Point.ByCoordinates(0, 0, 2) # establish a reference solid
ptEnd 		= Point.ByCoordinates(0, 0, 10) # that points up in z axis
radiusStart = 1
radiusEnd 	= 0.01 # cone needs to have end radius to not be a surface
solidCone 	= Cone.ByPointsRadii( # if a surface we cant change color
				ptStart, ptEnd, radiusStart, radiusEnd)

planes 		= [Plane.YZ(), Plane.XZ(), Plane.XY()] # Plane.ByOriginNormal
cs = [] # create empty list to store coordinate systems in
for p in planes : # alternative use CoordinateSystem.ByOriginVector
	cs.append(Plane.ToCoordinateSystem(p)) # transform plane into cs

trees = [] # create empty lists to store grey cones 'trees' in
for s in cs :
	trees.append(Geometry.Transform(solidCone, s)) # transform cone by cs

colorR 		= DSCore.Color.ByARGB(255, 255, 0, 0) # red
colorG 		= DSCore.Color.ByARGB(255, 0, 255, 0) # green
colorB 		= DSCore.Color.ByARGB(255, 0, 0, 255) # blue
colorRGB 	= [colorR, colorG, colorB] # red, green and blue

colorTrees  = [] # create an empty list to store coloured trees in
for t,c in zip(trees,colorRGB) : # use zip to access two lists
	colorTrees.append(GeometryColor.ByGeometryColor(t,c)) # color trees

keys 		= ['x-mas tree', 'y-mas tree', 'z-mas tree'] # define 'labels'
joke 		= dict(zip(keys, colorTrees)) # use dictionary to label trees

OUT = joke, colorTrees # output the joke and the coloured trees
