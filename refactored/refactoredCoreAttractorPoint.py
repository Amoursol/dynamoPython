"""
refactoredCoreAttractorPoint.py
-
a dynamoPython script, visit the website for more details
https://github.com/Amoursol/dynamoPython

node to code applied to sample file 'Core_AttractorPoint.dyn' 
with the resulting design script refactored as python
"""

__author__ = 'Adam Bear - adam@ukbear.com'
__twitter__ = '@adambear82'
__github__ = '@adambear82'
__version__ = '1.0.0'

"""
t1 = (1..50..5);
point1 = Point.ByCoordinates(t1<1>, t1<2>, 0);
t5 = List.Flatten(point1, -1);
t6 = 28.6701555980507;
t7 = 11.5011100116203;
point2 = Point.ByCoordinates(t6, t7, 0);
t8 = Geometry.DistanceTo(t5<1L>, point2<1L>);
x = t8;
t4 = x / 2;
vector1 = Vector.ByCoordinates(0, 0, t4);
point3 = Point.Add(t5, vector1);
x1 = t8;
t2 = x1 / 15;
cylinder1 = Cylinder.ByPointsRadius(t5, point3, t2);
"""

# Load the Python Standard and DesignScript Libraries
import sys
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

#t6 = 28.6701555980507;
#rename to anchorX
anchorX = 28.7
#t7 = 11.5011100116203;
#rename to anchorY
anchorY = 11.5
#point2 = Point.ByCoordinates(t6, t7, 0);
#rename to anchorPt
anchorPt = Point.ByCoordinates(anchorX, anchorY, 0)

#t1 = (1..50..5);
#replace design script range with python range & rename to gridRange
gridRange = range(1,50,5)

#create empty list to store cylinders
cylinders = []
for x in gridRange :
	for y in gridRange :
	
		#point1 = Point.ByCoordinates(t1<1>, t1<2>, 0);
		#remove replication guides, and rename to gridBasePt
		gridBasePt = Point.ByCoordinates(x, y, 0)
				
		#t8 = Geometry.DistanceTo(t5<1L>, point2<1L>);
		#find distance between anchor point and the current grid point
		gridDist = Geometry.DistanceTo(anchorPt, gridBasePt)
		
		#t4 = x / 2;
		vecFactor = gridDist / 2
		#t2 = x1 / 15;
		radFactor = gridDist / 15
		
		#vector1 = Vector.ByCoordinates(0, 0, t4);
		#refer to vecFactor & rename to vecPt
		vecPt = Vector.ByCoordinates(0, 0, vecFactor)

		#point3 = Point.Add(t5, vector1);
		#refer to gridBasePt, vecPt and rename to gridTopPt
		gridTopPt = Point.Add(gridBasePt, vecPt)
		
		#cylinder1 = Cylinder.ByPointsRadius(t5, point3, t2);
		#refer to variables and rename to cylinder
		cylinder = Cylinder.ByPointsRadius(gridBasePt, gridTopPt, radFactor)
		
		#add cylinder to list
		cylinders.append(cylinder)
		
# Assign your output to the OUT variable.
OUT = cylinders
