# (c) 2014-2025 CadQuery Developers

"""
CadQuery GUI init module for FreeCAD
This adds a workbench with a scripting editor to FreeCAD's GUI.
"""

import Part, FreeCAD, FreeCADGui
from CQGui.Command import CadQueryHelp, CadQueryClearOutput


class CadQueryWorkbench (Workbench):
    """CadQuery workbench for FreeCAD"""
    """CadQuery workbench for FreeCAD"""
      
    MenuText = "CadQuery"
    ToolTip = "CadQuery workbench"


    def Initialize(self):
        self.appendMenu('CadQuery', ['CadQueryClearOutput', 'CadQueryHelp'])


    def Activated(self):
        pass


    def Deactivated(self):
        pass


FreeCADGui.addCommand('CadQueryClearOutput', CadQueryClearOutput())
FreeCADGui.addCommand('CadQueryHelp', CadQueryHelp())

FreeCADGui.addWorkbench(CadQueryWorkbench())
