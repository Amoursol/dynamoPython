"""
CREATE STRUCTURAL BEAM WITHOUT ELEMENT BINDING
"""
__author__ = 'Sol Amour'
__version__ ='1.0.0'

# import common language runtime 
import clr
# Import necessary Revit API libraries for managing Documents and Transactions
clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
# Import the full Revit API
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *
# Import necessary Revit API Nodes, including Geometry Conversion methods
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

# Access the active Revit document (Project)
doc = DocumentManager.Instance.CurrentDBDocument

# Inputs from Dynamo, all unwrapped to expose Revit API methods, not Dynamo ones
dynCurve = UnwrapElement(IN[0])    # Dynamo Curve input
level = UnwrapElement(IN[1])       # Revit Level input
beamType = UnwrapElement(IN[2])    # Structural Framing Family Type input

# Debugging checks to ensure we have inputs
if dynCurve is None:
    OUT = "Input curve is null"    # Ensure the Curve input is fulfilled
elif level is None:
    OUT = "Level is null"          # Ensure the Level input is fulfilled
elif beamType is None:
    OUT = "Family Type is null"    # Ensure the Family Type input is fulfilled
else:
    # Implement a Try/Catch safeguard to return Error Messages if Python fails
    try:
        # Start a transaction to allow changes to be made to the Revit Document (Project)
        TransactionManager.Instance.EnsureInTransaction(doc)

        # Check that beamType is actually a FamilySymbol and of the correct category
        if isinstance(beamType, FamilySymbol) and beamType.Family.FamilyCategory.Name == "Structural Framing":
            
            # Ensure the family type is activated in the Revit Document
            if not beamType.IsActive:
                beamType.Activate() # Activiate it if not
                doc.Regenerate()    # Regenerate the Revit Document (Project) to ensure Dynamo can now see this Beam Type

            # Convert Dynamo Curve to Revit Curve using .ToRevitType(True) that stops Element Binding from occurring
            rvtCurve = dynCurve.ToRevitType(True)

            # Define structural type as of Beam type
            strucType = Structure.StructuralType.Beam

            # Create the structural beam in the Revit Document
            beam = doc.Create.NewFamilyInstance(rvtCurve, beamType, level, strucType)

            # Commit the transaction to make changes to the Revit Document (Project)
            TransactionManager.Instance.TransactionTaskDone()

            # Output the created beam from the Python node
            OUT = beam
        else:
            # Output error message if beamType is not correct
            OUT = "The specified type is not a valid Structural Framing Family Type."
    except Exception as e:
        # Catch any errors that occur during beam creation and output for debugging
        TransactionManager.Instance.TransactionTaskDone()
        OUT = "Error occurred: " + str(e)
