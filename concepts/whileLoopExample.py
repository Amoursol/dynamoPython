"""
PYTHON WHILE LOOP
"""
__author__ = 'Sol Amour - amoursol@gmail.com'
__twitter__ = '@solamour'
__version__ = '1.0.0'


# SYNTAX: while condition is true: do this
# While = This initialises the While Loop
# Condition is true: We specify a condition (parameters) under which our loop will run. 
# (NOTE: Make sure there is an 'exit' from this loop - or you will run into recursion 
# problems; Computer will keep computing forever - in essence freeze)
# Do this = Any action you wish to do while the condition is true

# NOTES:
# You must indent any Loop. Convention is to use 4x spaces, or a single tab.
# In order to return a result, you have to append a thing to an empty list to then 
# pass to the OUT port
# Spelling matters. Make sure your capitalisation is consistent
# While loops can be dangerous because they can have recursion issues. You always need 
# to set an 'exit' to your loop (A method of it stopping) or the computer will run into an 
# infinite loop and calculate forever (Freeze for all intents and purposes)

# IMPORTS / REFERENCES:
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *
import sys
sys.path.append(r'C:\Program Files (x86)\IronPython 2.7\Lib')
import random

# IN PORTS:
pointsList = IN[0] # Input a flat Points List

# An empty catchment list to which we append (Add) our results
result = []

# FOR LOOP:
for point in pointsList:
	# A random value to give our Cylinders height
	zValue = random.random() * 1000
	# We dont want any zValue of under 25, so we run a while loop to negate those outcomes. 
	# This means that while the result of our random number generator (Between zero and 100) 
	# has a result of under50, just run it again until it doesn't.
	while zValue < 250:
		# We then re-assign the variable 'zValue' to our new random number that sits between 
		# 50 and 100
		zValue = random.random() * 1000
		
	# We use DesignScript inside here to add a point by our vector and zValue random variable
	addPoint = point.Add( Vector.ByCoordinates( 0, 0, zValue ) )
	# We then generate a Cylinder for every point that passes our 'if' conditional check and 
	# give it a static radius of 2
	cyl = Cylinder.ByPointsRadius( point, addPoint, 20 )
	# In order to see this in Dynamo, we need to append the result to our catchment list called 
	# 'result'
	result.append( cyl )

# Then to push our loop results back to Dynamo, we assign our catchment list to the 'OUT' port
OUT = result