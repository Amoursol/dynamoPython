'''
Create Wall Sweep - By Wall
'''

__author__ = 'min.naung/mgjean @https://twentytwo.space/contact'
__twitter__ = '@_mgjean'
__version__ ='1.0.0'


# import common language runtime 
import clr

# clr.AddReference loads and imports .net assembly(dll) as python module
# load RevitAPI.dll and RevitServices.dll
clr.AddReference("RevitAPI")
clr.AddReference("RevitServices")

# import all classes from Revit DB
from Autodesk.Revit.DB import *

# import document manager
from RevitServices.Persistence import DocumentManager
# import transaction manager
from RevitServices.Transactions import TransactionManager

# instantiate current document
doc = DocumentManager.Instance.CurrentDBDocument

# for output result
wallSweeps = []
# wallsweeptype dictionary
wallSweepTypes = {"Sweep": WallSweepType.Sweep,
				  "Reveal": WallSweepType.Reveal}
# input1 walls
walls = IN[0]
# input3 string input
sweepOrReveal = IN[2]
# input4 boolean input default is horizontal(false)
vertical = IN[3] if IN[3] else False
# distance from wall base if horizontal, vertical wall start
# default is 1000mm
distance = IN[4]/304.8 if IN[4] else 1000/304.8

# check and make list
if not isinstance(walls,list):
	walls = UnwrapElement([IN[0]])
else:
	walls = UnwrapElement(IN[0])
# input2 wall sweep type input
wallSweepTypeId = UnwrapElement(IN[1]).Id
# wall sweep info class constructor
wallSweepInfo = WallSweepInfo(wallSweepTypes[sweepOrReveal],vertical)
# set distance
wallSweepInfo.Distance = distance
# start transaction
TransactionManager.Instance.EnsureInTransaction(doc)
# loop input walls
for wall in walls:
	# create wall sweep by wall, wallsweepid and wallsweep info
	wallsweep = WallSweep.Create(wall,wallSweepTypeId,wallSweepInfo)
	# append result to output
	wallSweeps.append(wallsweep)
# transaction done
TransactionManager.Instance.TransactionTaskDone()
# output result
OUT = wallSweeps