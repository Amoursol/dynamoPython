'''
CATEGORIES TO M SCRIPT - CREATE CONDITIONAL STATEMENT CODE FOR POWER BI
-
a dynamoPython script, visit the website for more details
https://github.com/Amoursol/dynamoPython
'''
__author__ = 'Adam Bear - adam@ukbear.com'
__twitter__ = '@adambear82'
__github__ = '@adambear82'
__version__ = '1.0.0'

'''
for large projects with lots of clashes it is useful to analyse in
a business inteligence or data visualisation tool such as ms power bi.
creating the conditonal statement in power bi can take a long time if
there are a lot of categories to include
'''

# ------------------------
# import modules
# ------------------------

# refer to the clipboard
import clr
clr.AddReference('System.Windows.Forms')
from System.Windows.Forms import Clipboard

# refer to the document manager
clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
doc = DocumentManager.Instance.CurrentDBDocument

# refer to the revit API
clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.DB import *

# ------------------------
# inputs & variables
# ------------------------

# some categoreies exported from navisworks are not included as
# categories in visibility graphics, for examplevv
# Handrails, Landings, Pads, Runs, Slab Edges, Top Rails, Wall Sweeps

# remove single and double spaces after commas and split into list
catsInput = IN[0]
catsReplace1 = catsInput.replace(', ', ',')
catsReplace2 = catsReplace1.replace(',  ', ',')
catsManual = catsReplace2.split(',')
catsManual.sort()

# provide reference strings
hashtag = 'Renamed Columns1'
pathlink = 'pathlink'
filterIn = 'filter_in'
filterOut = 'filter_out'

# ------------------------
# get categories
# ------------------------

# get categories that can add sub categories
# ie the categories which appear in vis graphics
# annotated from forum post with kudos to René Picazo
# https://forum.dynamobim.com/t/get-all-elements-in-model-categories/9447/7
modelCats = []
for cat in doc.Settings.Categories :
     if cat.CategoryType == CategoryType.Model and cat.CanAddSubcategory:
         modelCats.append(cat.Name)

# only append extra categories if they have been defined in input
if catsInput :
	for cat in catsManual :
		modelCats.append(cat)

# sort alphabetically so its easier to read
cats = sorted(modelCats)

# ------------------------
# strings
# ------------------------

# the 1st line adds a column to the table based on a filter on the hash
table = ''.join(('= Table.AddColumn(#"', hashtag, '", "filter",'))

# define strings to be used in M code
each = 'each if ['
elif0 = 'else if ['
elif1 = '] = "'
elif2 = '" then "'
elif3 = '"'

# the 2nd line is a special case
# where cats[0] requires 'each' instead of 'else if'
catJoin = each, pathlink, elif1, cats[0], elif2, filterIn, elif3
temp = ''.join(catJoin)
listLines = []
listLines.append(temp)

# the 3rd line and onwards starts with else if
# each row is checked if it is equall to one of the remaining cats
# cats is sliced by [1:] to return items from index 1 to the last index
for c in cats[1:] :
	catJoin = elif0, pathlink, elif1, c, elif2, filterIn, elif3
	temp = ''.join(catJoin)
	listLines.append(temp)
lines = '\r\n'.join(listLines)

# the final line starts with else
# rows not in cats are given the filterOut value
strElse = ''.join(('else "', filterOut, '")'))

# the code is brought together with new lines between each line
code = '\r\n'.join((table, lines, strElse))

# ------------------------
# send to clipboard
# ------------------------

# annotated with kudos to bakery 'by send to clipboard from revit' (sic)
# https://github.com/LukeyJohnson/BakeryForDynamo/blob/97e5622db7ba14cd42caac9b8bd4fdba6b66871e/nodes/bv%20Send%20to%20Clipboard%20from%20Revit.dyf#L5-L12
# try to copy the code, provide a message if it fails
try:
	Clipboard.SetText(code)
	copyMsg = code
except:
	copyMsg = 'Data could not be copied to clipboard'

# ------------------------
# output
# ------------------------

OUT = copyMsg
