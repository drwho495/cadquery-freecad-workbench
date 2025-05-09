# CQGui/CodeFeatureCommands.py
# -*- coding: utf-8 -*-

import FreeCAD # Required for FreeCAD.activeDocument(), FreeCAD.newDocument(), FreeCAD.GuiUp, FreeCAD.Console
import os # For path joining
# FreeCADGui is imported within functions after GuiUp check or if PySide is used.
# PySide.QtGui is imported within register_code_feature_command after GuiUp check.

# Import the core logic functions from CodeFeature.py
from .CodeFeature import createCodeFeature, executeCodeFeature

def registerCodeFeatureCommand():
    """
    Registers a command in FreeCAD to create a CodeFeature.
    This is a basic example; a real implementation would integrate into the CadQuery workbench menu.
    """
    if not FreeCAD.GuiUp: # Guard at the top
        return

    from PySide import QtGui # Imports moved up
    import FreeCADGui

    class CreateCodeFeatureCommand:
        def GetResources(self):
            return {"MenuText": "Create Code Feature",
                    "ToolTip": "Creates a new feature driven by CadQuery/Build123D code."}

        def Activated(self):
            doc = FreeCAD.activeDocument()
            if not doc:
                doc = FreeCAD.newDocument("CodeFeatureDoc")
            
            featureName, nameOk = QtGui.QInputDialog.getText(FreeCADGui.getMainWindow(), 
                                                          "Create Code Feature", 
                                                          "Enter feature name:", 
                                                          QtGui.QLineEdit.Normal, 
                                                          "MyCodeObject")
            if not (nameOk and featureName):
                FreeCAD.Console.PrintMessage("Code Feature creation cancelled by user (no name provided).\n")
                return

            macroFilename, macroOk = QtGui.QInputDialog.getText(FreeCADGui.getMainWindow(),
                                                                "Set Macro File (Optional)",
                                                                "Enter a macro name (e.g., MyShape)\nLocated in your default macro directory:",
                                                                QtGui.QLineEdit.Normal,
                                                                "") # Default empty
            
            newFeature = createCodeFeature(doc, name=featureName)
            if not newFeature:
                FreeCAD.Console.PrintError(f"Failed to create Code Feature object named {featureName}.\n")
                return

            if macroOk and macroFilename:
                try:
                    defaultMacroDir = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Macro").GetString("MacroPath")

                    newFeature.MacroDir = defaultMacroDir
                    if not defaultMacroDir:
                        FreeCAD.Console.PrintWarning("Default macro directory not found or not set in preferences.\n")
                    else:
                        if not macroFilename.endswith(".FCMacro"):
                            macroFilename += ".FCMacro"

                            newFeature.MacroFilename = macroFilename

                except Exception as e:
                    FreeCAD.Console.PrintError(f"Error getting default macro path or setting MacroPath property: {e}\n")
            
            executeCodeFeature(newFeature)

        def IsActive(self):
            return True
    
    FreeCADGui.addCommand('CQ_CreateCodeFeature', CreateCodeFeatureCommand())