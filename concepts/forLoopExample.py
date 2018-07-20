"""
PYTHON FOR LOOP
"""
__author__ = 'Sol Amour - amoursol@gmail.com'
__twitter__ = '@solamour'
__version__ = '1.0.0'

# SYNTAX: for thing in container: do this
# For = This initialises the loop
# Thing = A variable name that substitutes for every item inside your list
# In = Runs the loop for every item inside your container
# Container = The list, or container, of your items.
# colon ( : ) = This terminates the first line of the loop. All actions after 
# this occur on every item (thing) inside the list (container)
# Do this = Any action you wish to do to every item (thing) inside the list 
# (container)

# NOTES:
# You must indent any Loop. Convention is to use 4x spaces, or a single tab.
# In order to return a result, you have to append a thing to an empty list to 
# then pass to the OUT port
# Spelling matters. Make sure your capitalisation is consistent

# IMPORTS / REFERENCES:
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *
import sys
sys.path.append(r'C:\Program Files (x86)\IronPython 2.7\Lib')
import random

# IN PORTS:
pointsList = IN[0] #Input a flat list of points here

# An empty catchment list to which we append (Add) our results
result = []

# FOR LOOP:
for point in pointsList:
	# A random value to give our Cylinders height
	zValue = random.random() * 1000
	# If and only if the value of this is greater than 25 do we run this on 
	# our  points. This means we will always have a variable output number 
	# somewhere between 0 and 100. There is an implicit 'Else' here which 
	# simply means if it's under 25 pass over that point and do nothing.
	if zValue > 250:
		# We use DesignScript inside here to add a point by our vector and 
		# zValue random variable
		addPoint = point.Add( Vector.ByCoordinates( 0, 0, zValue ) )
		# We then generate a Cylinder for every point that passes our 'if' 
		# conditional check and give it a static radius of 2
		cyl = Cylinder.ByPointsRadius( point, addPoint, 20 )
		# In order to see this in Dynamo, we need to append the result to our 
		# catchment list called 'result'
		result.append( cyl )

# Then to push our loop results back to Dynamo, we assign our catchment list 
# to the 'OUT' port
OUT = result