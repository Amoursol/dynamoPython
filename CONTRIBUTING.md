# CONTRIBUTING
When contributing to this repository & community with a script or Dynamo file, please follow the requirements below. We ask for these things so we can ensure a consistently high quality of materials, making it easier for everyone to learn & use Python inside Dynamo.

### Principles

All contributions need to make sure :
  - code can be copy and pasted into Python script nodes inside of Dynamo
  - the python scripts will work without needing modification, assuming correct information is passed into the input ports
  - any external dependencies or libraries that are required are clearly identified in the script notes and further instructions provided
  - most of all, the contribution provides educational value and is as accessible to all
  
### Annotations
All scripts and Dynamo files should be heavily **Annotated** as the main intention of this resource is to educate.

A few things to keep in mind when writing annotations : 
- annotations should explain __WHY__ something is done that way or is required, for example : 
```python
# we need to import the common language runtime to be able to interact with Dynamo & Revit
import clr
```
and another :
```python
# python includes a definition of PI in its math library, so we import it
import math
# we only need PI accurate to the first 2 decimal places
# so we round it down and store it in a variable called pi
pi = round(math.pi,2)
```
- only explain __WHAT__ the code is doing when it's not evident from the code itself.

for example, don't do this :
```python
# initialise a
a = 3.14
```
but instead do this
```python
# we store a rounded down value of PI in a variable called a
a = 3.14
```

### Code style
We generally recommed following the in-depth [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/) when writing Python code.

All code lines to be limited to a maximum of 79 characters as per the [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/?#maximum-line-length)

For flowing long blocks of text with fewer structural restrictions (`docstrings` or `comments`), the line length should be limited to 72 characters.

If you wish to run an online check to conform with PEP 8, then you can use [this Link](http://pep8online.com/) to check your Python online. Please note that the following **Syntax** section is somewhat different to PEP-8. 

## Template
If you wish to contribute, please follow the general script template below:

```python
"""
NAME OF MODULE
-
a dynamoPython script, visit the website for more details
https://github.com/Amoursol/dynamoPython
"""
__author__ = 'author - email'
__twitter__ = '@twitter handle'
__github__ = '@github handle'
__version__ = 'version of script'

"""
Script Notes/Information
"""

Script Body
```

### An example of such is as follows:

```python
"""
LIST: ADD ITEM TO FRONT
-
a dynamoPython script, visit the website for more details
https://github.com/Amoursol/dynamoPython
"""
__author__ = 'Sol Amour - amoursol@gmail.com'
__twitter__ = '@solamour'
__github__ = '@Amoursol'
__version__ = '1.0.0'

"""
SYNTAX: List.insert(index, item)
List = The list to which you want to insert an item
.insert = The insert function which requires two input variables
index = The index where you wish to insert your new item
item = The item which you wish to insert into your list
"""

insertItem = ["X", 3]  # A list of elements to insert
baseList = [["A", 11], ["B", 7], ["C", 9]]  # A data list of lists
# (Paired alphabetic and numeric characters)

baseList.insert(0, insertItem)  # We want to insert our 'insertItem'
# into our 'baseList', so we call the function '.insert' on our
# 'baseList' and choose an index of '0' (Add Item to Front)

OUT = baseList

```
