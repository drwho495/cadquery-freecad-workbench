import FreeCAD
import Part
from io import BytesIO
import os
import cadquery as cq

part = None

def getShape(part_param):
    brep_stream = BytesIO()
    if isinstance(part_param, cq.Workplane):
        part_param.val().exportBrep(brep_stream)
    elif isinstance(part_param, cq.Shape):
        part_param.exportBrep(brep_stream)
    elif hasattr(part_param, "wrapped"):
        from build123d import export_brep
        export_brep(part_param, brep_stream)
    elif hasattr(part_param, "part") and hasattr(part_param.part, "wrapped"):
        from build123d import export_brep
        export_brep(part_param.part, brep_stream)
    else:
        return None
    brep_string = brep_stream.getvalue().decode('utf-8')
    part_shape = Part.Shape()
    part_shape.importBrepFromString(brep_string)
    return part_shape

def upload_part(newObj):
    global part
    part = newObj

def createCodeFeature(doc, name="CodeFeature"):
    if not doc: return None
    obj = doc.addObject("Part::FeaturePython", name)
    if not obj: return None
    obj.addProperty("App::PropertyString", "MacroFilename", "CodeObject", "")
    obj.addProperty("App::PropertyPath", "MacroDir", "CodeObject", "")
    obj.addProperty("App::PropertyString", "GeneratedObjectLabel", "CodeObject", "")
    obj.MacroFilename = ""
    try: obj.MacroDir = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Macro").GetString("MacroPath")
    except: obj.MacroDir = ""
    obj.GeneratedObjectLabel = name
    ViewProviderCodeFeature(obj.ViewObject)
    CodeFeatureProxy(obj)
    return obj

def executeCodeFeature(featureObject):
    global part
    if not hasattr(featureObject, "MacroFilename"):
        try:
            featureObject.addProperty("App::PropertyString", "MacroFilename", "CodeObject", "")
            featureObject.MacroFilename = ""
        except: return
    if not hasattr(featureObject, "MacroDir"):
        try:
            featureObject.addProperty("App::PropertyPath", "MacroDir", "CodeObject", "")
            try: featureObject.MacroDir = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Macro").GetString("MacroPath")
            except: featureObject.MacroDir = ""
        except: return

    macroFilename = featureObject.MacroFilename
    macroDir = str(featureObject.MacroDir)
    if not macroFilename: return

    fullMacroPath = ""
    if os.path.isabs(macroFilename): fullMacroPath = macroFilename
    elif macroDir and os.path.isabs(macroDir): fullMacroPath = os.path.join(macroDir, macroFilename)
    elif macroDir: fullMacroPath = os.path.join(macroDir, macroFilename)
    else:
        doc = featureObject.Document
        if doc and doc.FileName:
            docDir = os.path.dirname(doc.FileName)
            testPath = os.path.join(docDir, macroFilename)
            if os.path.exists(testPath): fullMacroPath = testPath
        if not fullMacroPath:
            try:
                userMacroDir = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Macro").GetString("MacroPath")
                if userMacroDir:
                    testPath = os.path.join(userMacroDir, macroFilename)
                    if os.path.exists(testPath): fullMacroPath = testPath
            except: pass
        if not fullMacroPath and os.path.exists(macroFilename): fullMacroPath = macroFilename
            
    if not fullMacroPath or not os.path.exists(fullMacroPath):
        FreeCAD.Console.PrintError(f"Macro file not found: {macroFilename} for {featureObject.Label}\n")
        return
        
    codeFromFile = ""
    try:
        with open(fullMacroPath, 'r', encoding='utf-8') as f: codeFromFile = f.read()
    except Exception as e:
        FreeCAD.Console.PrintError(f"Error reading macro {fullMacroPath}: {e}\n")
        return

    part = None 
    execGlobals = {"__builtins__": __builtins__, "FreeCAD": FreeCAD, "App": FreeCAD, "upload_part_to_feature": upload_part}
    if FreeCAD.GuiUp:
        import FreeCADGui
        execGlobals["FreeCADGui"] = FreeCADGui
        execGlobals["Gui"] = FreeCADGui
    
    localScope = {}

    try:
        exec(codeFromFile, execGlobals, localScope)
        
        current_shape = None
        if part is not None:
            current_shape = getShape(part)
        else:
            result_val = localScope.get('result')
            if result_val is not None:
                current_shape = getShape(result_val)
            else:
                 FreeCAD.Console.PrintWarning(f"Macro {macroFilename} did not call upload_part_to_feature() nor set a 'result' variable.\n")

        if current_shape and not current_shape.isNull():
            featureObject.Shape = current_shape
        elif part is not None or localScope.get('result') is not None: # It tried to produce something but it was invalid
            FreeCAD.Console.PrintError(f"Macro {macroFilename} did not produce a valid shape.\n")
        
        if hasattr(featureObject, "GeneratedObjectLabel"):
            if featureObject.GeneratedObjectLabel: featureObject.Label = featureObject.GeneratedObjectLabel
            else: featureObject.Label = featureObject.Name

    except Exception as e:
        import traceback
        FreeCAD.Console.PrintError(f"Error executing macro {fullMacroPath}:\n{traceback.format_exc()}\n")
    finally:
        if FreeCAD.ActiveDocument: FreeCAD.ActiveDocument.recompute()

class ViewProviderCodeFeature:
    def __init__(self, vobj):
        vobj.Proxy = self
        self.ViewObject = vobj
    def attach(self, vobj): self.__init__(vobj)
    def updateData(self, fp, prop): pass
    def getDisplayModes(self, obj): return ["Shaded", "Wireframe"]
    def setDisplayMode(self, mode): return mode
    def getIcon(self): return ""
    def __getstate__(self): return None
    def __setstate__(self, state): return None

class CodeFeatureProxy:
    def __init__(self, obj):
        self.Object = obj
        obj.Proxy = self
    def execute(self, fp):
        executeCodeFeature(fp)
        return True
    def onChanged(self, fp, prop):
        if prop == "MacroFilename" or prop == "MacroDir" or prop == "GeneratedObjectLabel":
            fp.touch()
    def __getstate__(self): return None
    def __setstate__(self, state): return None
