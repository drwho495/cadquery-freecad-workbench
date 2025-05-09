# CQGui/CodeFeatureCommands.py
# -*- coding: utf-8 -*-

import FreeCAD # Required for FreeCAD.activeDocument(), FreeCAD.newDocument(), FreeCAD.GuiUp, FreeCAD.Console
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
            
            feature_name, ok = QtGui.QInputDialog.getText(FreeCADGui.getMainWindow(), 
                                                          "Create Code Feature", 
                                                          "Enter feature name:", 
                                                          QtGui.QLineEdit.Normal, 
                                                          "MyCodeObject")
            if ok and feature_name:
                new_feature = create_code_feature(doc, name=feature_name)
                if new_feature:
                    execute_code_feature(new_feature) 
                    if FreeCAD.ActiveDocument: FreeCAD.ActiveDocument.recompute()
            else:
                FreeCAD.Console.PrintMessage("Code Feature creation cancelled by user.\\n")

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
                FreeCAD.Console.PrintWarning("No object selected to recompute.\\n")
                return
            
            recomputed_any = False
            for obj in selection:
                if hasattr(obj, "MacroPath"): 
                    FreeCAD.Console.PrintMessage(f"Attempting to recompute Code Feature {obj.Label}.\\n")
                    execute_code_feature(obj)
                    recomputed_any = True

            if not recomputed_any:
                 FreeCAD.Console.PrintWarning("No selected object appears to be a Code Feature (has MacroPath property).\\n")

        def IsActive(self):
            selection = FreeCADGui.Selection.getSelection()
            if not selection: return False
            for obj in selection:
                if hasattr(obj, "MacroPath"):
                    return True
            return False
            
    FreeCADGui.addCommand('CQ_RecomputeCodeFeature', RecomputeCodeFeatureCommand())
