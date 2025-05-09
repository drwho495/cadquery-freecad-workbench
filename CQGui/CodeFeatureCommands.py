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
            
            # Get feature name
            featureName, nameOk = QtGui.QInputDialog.getText(FreeCADGui.getMainWindow(), 
                                                          "Create Code Feature", 
                                                          "Enter feature name:", 
                                                          QtGui.QLineEdit.Normal, 
                                                          "MyCodeObject")
            if not (nameOk and featureName):
                FreeCAD.Console.PrintMessage("Code Feature creation cancelled by user (no name provided).\n")
                return

            # Create the feature first
            newFeature = createCodeFeature(doc, name=featureName)
            if not newFeature:
                FreeCAD.Console.PrintError(f"Failed to create Code Feature object named {featureName}.\n")
                return

            # Optionally, ask for macro filename
            macroFilename, macroOk = QtGui.QInputDialog.getText(FreeCADGui.getMainWindow(),
                                                                "Set Macro File (Optional)",
                                                                "Enter a macro name (e.g., MyShape)\nLocated in your default macro directory:",
                                                                QtGui.QLineEdit.Normal,
                                                                "") # Default empty

            if macroOk and macroFilename:
                try:
                    defaultMacroDir = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Macro").GetString("MacroPath")
                    if not defaultMacroDir:
                        FreeCAD.Console.PrintWarning("Default macro directory not found or not set in preferences.\n")
                    else:
                        fullMacroPath = os.path.join(defaultMacroDir, macroFilename)
                        if not fullMacroPath.endswith(".FCMacro"):
                            fullMacroPath += ".FCMacro"

                        newFeature.MacroPath = fullMacroPath
                        
                        if not os.path.exists(fullMacroPath):
                             FreeCAD.Console.PrintWarning(f"Warning: Macro file {fullMacroPath} does not currently exist.\n")
                except Exception as e:
                    FreeCAD.Console.PrintError(f"Error getting default macro path or setting MacroPath property: {e}\n")
            
            executeCodeFeature(newFeature)
            if FreeCAD.ActiveDocument: FreeCAD.ActiveDocument.recompute()

        def IsActive(self):
            return True
    
    FreeCADGui.addCommand('CQ_CreateCodeFeature', CreateCodeFeatureCommand())


def recomputeSelectedCodeFeatureCommand():
    """
    Registers a command to recompute the selected CodeFeature.
    """
    if not FreeCAD.GuiUp: # Guard at the top
        return

    import FreeCADGui # Import moved up

    class RecomputeCodeFeatureCommand:
        def GetResources(self):
            return {"MenuText": "Recompute Code Feature",
                    "ToolTip": "Re-executes the code for the selected Code Feature."}

        def Activated(self):
            selection = FreeCADGui.Selection.getSelection()
            if not selection:
                FreeCAD.Console.PrintWarning("No object selected to recompute.\n")
                return
            
            recomputed_any = False
            for obj in selection:
                if hasattr(obj, "MacroPath"): 
                    FreeCAD.Console.PrintMessage(f"Attempting to recompute Code Feature {obj.Label}.\n")
                    execute_code_feature(obj)
                    recomputed_any = True

            if not recomputed_any:
                 FreeCAD.Console.PrintWarning("No selected object appears to be a Code Feature (has MacroPath property).\n")

        def IsActive(self):
            selection = FreeCADGui.Selection.getSelection()
            if not selection: return False
            for obj in selection:
                if hasattr(obj, "MacroPath"):
                    return True
            return False
            
    FreeCADGui.addCommand('CQ_RecomputeCodeFeature', RecomputeCodeFeatureCommand())
