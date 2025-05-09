import FreeCAD
import Part
from .CodeFeatureUtils import getShape, getPart, upload_part
from .SketchConverter import FreeCAD_Sketch
import os

# Method that will be used in the macros to update the Shape of a codefeature
class ViewProviderCodeFeature:
    def __init__(self, vobj):
        vobj.Proxy = self
        self.Object = vobj.Object

    def attach(self, vobj):
        self.Object = vobj.Object
        self.ViewObject = vobj
        return

    def updateData(self, fp, prop):
        pass

    def getDisplayModes(self, obj):
        modes = ["Shaded", "Wireframe", "Flat Lines", "Points"]
        return modes

    def setDisplayMode(self, mode):
        return mode

    def getIcon(self):
        # Return a custom icon (optional)
        return """
            /* XPM */
            static const char *icon[] = {
            "16 16 2 1",
            "  c None",
            ". c #0000FF",
            "                ",
            "       ..       ",
            "      ....      ",
            "     ......     ",
            "    ........    ",
            "   ..........   ",
            "  ............  ",
            " .............. ",
            " .............. ",
            "  ............  ",
            "   ..........   ",
            "    ........    ",
            "     ......     ",
            "      ....      ",
            "       ..       ",
            "                "
            };
        """
    
    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None
    
class CodeFeatureProxy:
    def __init__(self, obj):
        self.Object = obj
        obj.Proxy = self
    
    def updateFeature(self, obj):
        if not hasattr(obj, "MacroFilename"):
            try:
                obj.addProperty("App::PropertyString", "MacroFilename", "CodeObject", "Filename of the .FCMacro (e.g., MyMacro.FCMacro).")
                obj.MacroFilename = "" # Initialize
            except Exception as e:
                FreeCAD.Console.PrintError(f"Could not add MacroFilename property to {obj.Name}: {e}")
                return
                
        if not hasattr(obj, "MacroDir"):
            try:
                obj.addProperty("App::PropertyPath", "MacroDir", "CodeObject", "Directory containing the macro file. Leave empty or set to user/doc default.")
                try:
                    defaultMacroUserPath = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Macro").GetString("MacroPath")
                    obj.MacroDir = defaultMacroUserPath
                except:
                    obj.MacroDir = ""
            except Exception as e:
                FreeCAD.Console.PrintError(f"Could not add MacroDir property to {obj.Name}: {e}")
                return

        macroFilename = obj.MacroFilename
        macroDir = obj.MacroDir

        if not macroFilename:
            FreeCAD.Console.PrintError(f"MacroFilename property is empty for {obj.Name}. Please specify a .FCMacro filename.")
            return

        fullMacroPath = ""

        if os.path.isabs(macroFilename):
            fullMacroPath = macroFilename
        elif macroDir and os.path.isabs(str(macroDir)):
            fullMacroPath = os.path.join(str(macroDir), macroFilename)
        elif macroDir: 
            fullMacroPath = os.path.join(str(macroDir), macroFilename)
        
        if fullMacroPath and os.path.exists(fullMacroPath):
            exec(open(fullMacroPath).read())

            part = getPart()

            if part != None:
                obj.Shape = getShape(part)
            else:
                FreeCAD.Console.PrintWarning("No part was uploaded!")

    def execute(self, obj):
        self.updateFeature(obj)
        return True

    def onChanged(self, fp, prop):
        if prop == "CodeString" or prop == "CodeType" or prop == "GeneratedObjectLabel":
            pass

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None