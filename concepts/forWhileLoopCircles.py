"""
PYTHON FOR/WHILE LOOP: BROKEN CIRCLES
"""
__author__ = 'Sol Amour - amoursol@gmail.com'
__twitter__ = '@solamour'
__version__ = '1.0.0'

# SYNTAX: for thing in container: do this
# For = This initialises the For Loop
# Thing = A variable name that substitutes for every item inside your list
# In = Runs the loop for every item inside your container
# Container = The list, or container, of your items.
# colon ( : ) = This terminates the first line of the loop. All actions after this 
# occur on every item (thing) inside the list (container)
# Do this = Any action you wish to do to every item (thing) inside the list (container)

# SYNTAX: while condition is true: do this
# While = This initialises the While Loop
# Condition is true: We specify a condition (parameters) under which our loop will run. 
# (NOTE: Make sure there is an 'exit' from this loop - or you will run into recursion 
# problems; Computer will keep computing forever - in essence freeze)
# Do this = Any action you wish to do while the condition is true

# NOTES:
# You must indent any Loop. Convention is to use 4x spaces, or a single tab.
# In order to return a result, you have to append a thing to an empty list to then pass 
# to the OUT port
# Spelling matters. Make sure your capitalisation is consistent
# While loops can be dangerous because they can have recursion issues. You always need to 
# set an 'exit' to your loop (A method of it stopping) or the computer will run into an 
# infinite loop and calculate forever (Freeze for all intents and purposes)

# IMPORTS / REFERENCES:
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *
clr.AddReference('DSCoreNodes')
from DSCore import Math
import sys
sys.path.append(r'C:\Program Files (x86)\IronPython 2.7\Lib')
import random

# IN PORTS:
originPoint = IN[0] # Center Point for our Circle (i.e Autodesk.Point.ByCoordinates() )
initialRadius = IN[1] # Base Radius (i.e 1000)
amount = IN[2] # Integer Slider (i.e 3 to 20)

# An empty catchment list to which we append (Add) our results
result = []

# FOR LOOP:
# For every single item (number) in a range (Zero to amount) do the following...
for number in range( amount ):
	# Define a radius as the initital radius multiplied by the number + 1 (To alleviate 
	# issues with multiplication of zero)
	radius = initialRadius * ( number + 1 )
	# Creating a random start angle between 0 and 180
	startAngle = random.random() * 180
	# Creating a random end angle between 0 and 360
	endAngle = random.random() * 360
	# Defining our Normal as vertical up the Z-Axis
	normal = Vector.ByCoordinates( 0, 0, 1 )
	# WHILE LOOP: 
	#We always want our 'End Angle' to be greater than our 'Start Angle', so we run a 
	# conditional 'While Loop' over it that states: While the endAngle is smaller than the 
	# startAngle, re-run our random number generator to give us a value between 0 and 360 
	# degrees
	while endAngle < startAngle:
		endAngle = random.random() * 360
	# After ensuring we don't have an End Angle less than our Start Angle, we generate an 
	# Arc based on the above properties.
	arc = Arc.ByCenterPointRadiusAngle( originPoint, radius, startAngle, endAngle, normal) 
	# We then append this arc back to our result list.
	result.append( arc )

# Then to push our loop results back to Dynamo, we assign our catchment list to the 'OUT' port
OUT = result