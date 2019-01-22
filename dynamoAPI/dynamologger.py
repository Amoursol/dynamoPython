"""
Export DATA to Server for Dynamo Usage Tracking
-
a dynamoPython script, visit the website for more details
https://github.com/Amoursol/dynamoPython
"""
__author__ = 'Timon Hazell'
__twitter__ = '@tmnhzll'
__github__ = '@thazell'
__version__ = '1.0.0'

"""
#The purpose of this script is to allow users to track usage of dynamo.
#The user needs to set the directory below and then it can be copied to all the scripts in the office.
#It will create a single json or CSV per dynamo run (so expect tons of files)
#The single file per run was selected to limit issues with writing to the same file, which occurred on the creators' network.
#Note if a script runs 30x in one session, each run will be logged, so consider that when working.
"""

# 
# ------------------Header - Import Section
import sys
import clr


sys.path.append(r'C:\Program Files (x86)\IronPython 2.7\Lib')
import os  

# Adding the DynamoRevitDS.dll module to work with the Dynamo API
clr.AddReference('DynamoRevitDS')
import Dynamo 

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit import DB

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager


doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

try:
    runscript = IN[0]
except:
    runscript = True

if runscript:

    #----------------Stored Variables Section

    # -->>>> update this string below to a network folder that all users have write access to
    networkFolder = r'C:\Temp\logreports\DynamoLogReports\''

    #Time saveed is assumed based on the following example:
    #If you expect that every time you renumber sheets you save 5 minutes, but if you renumber 500 sheets you save 5 minutes + 10 seconds per sheet * 500 sheets)
    #edit the following values for each script as an estimate.
    estimatedtimesavedeachrun = 10 #put the number of seconds this script will save the office every time it runs
    timesavedperelement = 0 #put the number of seconds this script will save for every element that gets edited. 


    releasedOrTesting = "Testing"
    exportAsJson = False #choose whether to record as a json (True) or csv (False)

    #try:
    import datetime
    #add date and time to and central file name subdirectory


    #--------------------Processing Section

    #get current time of dynamo run
    dtstampstring = str(datetime.datetime.today())

    #get computername of run
    computername = os.environ['COMPUTERNAME']

    #get windows username
    username = os.environ['USERNAME']

    #get dynamo filename

    # access to the current Dynamo instance and workspace
    dynamoRevit = Dynamo.Applications.DynamoRevit()
    currentWorkspace = dynamoRevit.RevitDynamoModel.CurrentWorkspace

    # access current version of dynamo
    version=dynamoRevit.RevitDynamoModel.Version

    # checks version of dynamo and adjusts output according to version
    if version.StartsWith("1."):

        # Gets file name which includes full path
        filename=currentWorkspace.FileName
        # Splits out file path to just file name
        dynamoFileName=filename.Split("\\")[-1].Replace(".dyn","")

    elif version.StartsWith("2."):
        dynamoFileName=currentWorkspace.Name
    else:
        dynamoFileName="Unkown"

    #get revit projectnumber
    projectnumber = doc.ProjectInformation.Number

    #get revit projectname
    projectname = doc.ProjectInformation.Name

    #get revit year
    revitYear = app.VersionNumber

    #get full revit version
    revitfullversion = app.VersionBuild

    #get revit saved filename or use 
    try:
        rvtfilename = doc.Title
    except:
        rvtfilename = "Unkown" # file may not be saved
        
    #calculate time saved per run:
    #current time saves per run is just an estimate.  
    #The user can use the following code if they want to count the number of elements 
    #that were processed in dynamo
    # and use that list to figure out the time savings per element
    try:
        dynamoelementsupdated = IN[1]
        if isinstance(dynamoelementsupdated,list):
            elementsupdated = len(dynamoelementsupdated)
        elif isinstance(dynamoelementsupdated, int):
            elementsupdated = dynamoelementsupdated
        elif isintance(dynamoelementsupdated, float):
            elementsupdated = dynamoelementsupdated
        elif   isintance(dynamoelementsupdated, str):
            elementsupdated = int(dynamoelementsupdated)
        else:
            elementsupdated = 0
    except:
        elementsupdated = 0

    timeSavedPerRun = estimatedtimesavedeachrun + timesavedperelement * elementsupdated
    #--------------------Output Section


    #create a dictionary which will be sent to a seperate file for each dynamo run
    outputdictionary = {}
    outputdictionary["Computer"] = computername
    outputdictionary["DynamoFile"] = dynamoFileName
    outputdictionary["Project Name"] = projectname
    outputdictionary["Project Number"] = projectnumber
    outputdictionary["Active Revit Project File Name"] = rvtfilename
    outputdictionary["Released or Testing"] = releasedOrTesting
    outputdictionary["Revit Version"] = revitYear
    outputdictionary["Revit Version Full Build"] = revitfullversion
    outputdictionary["TimeSaved (sec)"] = timeSavedPerRun
    outputdictionary["TimeStamp"] = dtstampstring
    outputdictionary["User"] = username


    #set directory, create directory if it doesn't exist:
    directory = networkFolder + computername + '\\'
        
    if not os.path.exists(directory):
        os.mkdir(directory)
    newfilename = str(datetime.datetime.today()).replace(" ","-").replace(":","-").replace(".","-") + ""


    if exportAsJson:
        import json
        #export json

        newfilename += "-logger.json"
        #create json file.  a new file will be created every time.  This was found to be the most consistent way of getting every run recorded.  

        with open(directory + newfilename, 'w') as fp:
            #OUT =  outputdictionary
            jsonstring = json.dumps(outputdictionary, indent=4)
            fp.write(jsonstring)   
        
    else:
        import csv
        
        newfilename += "-logger.csv"
        #create json file.  a new file will be created every time.  This was found to be the most consistent way of getting every run recorded.  

        
        with open(directory + newfilename, 'wb') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                fieldnames = outputdictionary.keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()  
                writer.writerow(outputdictionary)


    outputpreviewlist = []
    outputpreviewlist.append("The following was recorded to file:")
    outputpreviewlist.append(directory + newfilename)
    for title in outputdictionary.keys():
        outputpreviewlist.append("{0}: {1}".format(title,outputdictionary[title]))
    OUT = outputpreviewlist

    #if you want to see the output file, uncomment the following lines of code.
    #import subprocess
    #os.startfile(directory + newfilename)

    #-----------------Some code was based on work and questions on the forums by these people, thank you
    #John Pierson
    #Brendan Cassidy