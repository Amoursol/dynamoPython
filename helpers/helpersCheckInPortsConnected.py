'''
CHECK IN[PORTS] ARE CONNECTED & REPORT ERRORS
'''
__author__ = 'Adam Bear - adam@ukbear.com'
__twitter__ = '@adambear82'
__version__ = '1.0.0'

# IN[0] bool controls is python should be run
runBool = IN[0]
# IN[0], IN[1], IN[3] data inputs
data1 = IN[1]
data2 = IN[2]
data3 = IN[3]
# create a list of the data inputs
inputs = data1, data2, data3
# create a list of the port numbers of the inputs
inputRange = 1,2,3
# create a list of names for the data inputs
inputNames = "data one", "data two", "data three"
# create an empty list that will contain any error report
errorReport = []
# if the run bool is false then
if not runBool :
# append to the error report that the python is switched off
	errorReport.append("switched off @ IN[0]")
# if the run bool is true then
else :
# for each index in the zip use a variable (i,j,k)
	for i,j,k in zip(inputs,inputNames,inputRange) :
# if an IN[port] 'i' is not connected then
		if not i :
# append to the error report that
			errorReport.append( \
# there are no data conected to the input name 'j' at port number 'k'
			"no values in " + str(j) + " @ IN[" + str(k) + "]" \
# the backslash is an escape key, for new lines to be added for legibility
			)
# if the error report is empty then
if len(errorReport) == 0:
# try setting the output as the addition of data inputs
	try :
		output = data1 + data2 + data3
# if its not possible to add the data inputs (eg. integer + string)
	except Exception,e :
# set the output as the exception as a string
		output = e.ToString()
# if the error report is empty then
if len(errorReport) == 0 :
# send the output to the OUT port
	OUT = output
# if the error report is not empty then
else :
# send the error report to the OUT port
	OUT = errorReport
