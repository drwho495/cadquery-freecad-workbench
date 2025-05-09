from CQGui.display import show_object
from CQGui.CodeFeatureUtils import upload_part
from CQGui.SketchConverter import FreeCAD_Sketch

# Register the show_object function as a global function
globals()['show_object'] = show_object
globals()['upload_part'] = upload_part
globals()['FreeCAD_Sketch'] = FreeCAD_Sketch