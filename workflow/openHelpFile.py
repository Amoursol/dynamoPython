'''
OPEN HELP FILE - FOR SPECIFIED FILE WITH BOOL TOOGLE
-
a dynamoPython script, visit the website for more details
https://github.com/Amoursol/dynamoPython
'''
__author__ = 'Adam Bear - adam@ukbear.com'
__twitter__ = '@adambear82'
__github__ = '@adambear82'
__version__ = '1.0.0'

'''
When putting together a graph.dyn for use in dynamo player sometimes it
is usefull to give the user the option to open a help file associated
with the graph. This script will open a web page / pdf / other file if
a boolean toogle switch is set to true
'''

# when installing python by default a number of useful modules also get
# installed at the same time to a default library location. Although
# useful you wouldn't want to always use them so they are not built in
# to python and instead need to be imported, the first step is to
# import the sys module
import sys
# now we can define where to look for a library of useful moduels
pythonPath = 'C:\\Program Files (x86)\\IronPython 2.7\\Lib'
# appending pythonPath to sys path allow us to import modules from there
sys.path.append(pythonPath)
# importing the web browser from library allows us to open any file
import webbrowser

# in the dynamo workspace wire a boolean true / false toogle to input
# renaming the node will change the title of the switch in dynamo player
# changing it to something like the below
# switch toggle to True to open a help file for this Dynamo Player Graph
toggleBool = IN[0]
# in the dynamo worspace wire a string of a help file path to input
helpFile = IN[1]

# use 'if' so the script wil behave differently depending on the bool
if toggleBool :

	# if  a help file has been specified
	if helpFile :
		# open the help file
		webbrowser.open(helpFile)
		# provide help message
		msg = 'web page opened:\n' + helpFile

	# if a help file has not been specified
	else :
		# provide a help message
		msg = 'to open a help file:\n\
        connect a string containing\n\
        file to IN port IN[1]'

# if toggle bool false
else :
    # provide help message
    msg = 'to open help file:\nset bool to true'

# send help message to OUT port
OUT = msg
