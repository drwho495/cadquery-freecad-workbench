# (c) 2014-2025 CadQuery Developers

"""
CadQuery GUI init module for FreeCAD
This adds a workbench with a scripting editor to FreeCAD's GUI.
"""

import Part, FreeCAD, FreeCADGui
from FreeCADGui import Workbench # Import Workbench
from CQGui.Command import (CadQueryHelp,
                          CadQueryClearOutput,
                          CadQueryStableInstall,
                          CadQueryUnstableInstall,
                          Build123DInstall)
from CQGui.CodeFeatureCommands import registerCodeFeatureCommand, recomputeSelectedCodeFeatureCommand


class CadQueryWorkbench (Workbench):
    """CadQuery workbench for FreeCAD"""
      
    MenuText = "CadQuery"
    ToolTip = "CadQuery workbench"


    def Initialize(self):
        self.appendMenu('CadQuery', ['CQ_CreateCodeFeature']) 
        self.appendMenu('CadQuery', ['CQ_RecomputeCodeFeature']) 
        self.appendMenu('CadQuery', ['CadQueryClearOutput'])
        self.appendMenu(['CadQuery', 'Install'], ["CadQueryStableInstall",
                                                  "CadQueryUnstableInstall",
                                                  "Build123DInstall"])
        self.appendMenu('CadQuery', ['CadQueryHelp'])


    def Activated(self):
        pass


    def Deactivated(self):
        pass



FreeCADGui.addCommand('CadQueryStableInstall', CadQueryStableInstall())
FreeCADGui.addCommand('CadQueryUnstableInstall', CadQueryUnstableInstall())
FreeCADGui.addCommand('Build123DInstall', Build123DInstall())
FreeCADGui.addCommand('CadQueryClearOutput', CadQueryClearOutput())
FreeCADGui.addCommand('CadQueryHelp', CadQueryHelp())

# Register new commands from CodeFeature.py
# These functions internally call FreeCADGui.addCommand
if FreeCAD.GuiUp: # Ensure GUI is up before trying to register GUI commands
    registerCodeFeatureCommand()
    recomputeSelectedCodeFeatureCommand()

FreeCADGui.addWorkbench(CadQueryWorkbench())
