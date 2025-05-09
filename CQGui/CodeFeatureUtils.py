import FreeCAD
import Part

part = None

def getPart():
    global part

    return part

def getShape(part):
    import cadquery as cq
    from PySide import QtGui

    from io import BytesIO
    brep_stream = BytesIO()

    if isinstance(part, cq.Workplane):
        part.val().exportBrep(brep_stream)
    elif isinstance(part, cq.Shape):
        part.exportBrep(brep_stream)
    elif hasattr(part, "wrapped"):
        from build123d import export_brep

        export_brep(part, brep_stream)
    elif hasattr(part, "part") and hasattr(part.part, "wrapped"):
        from build123d import export_brep

        export_brep(part.part, brep_stream)
    else:
        print("Object type not support for display: ", type(part).__name__)
        return

    brep_string = brep_stream.getvalue().decode('utf-8')
    part_shape = Part.Shape()
    part_shape.importBrepFromString(brep_string)

    return part_shape

def upload_part(newObj):
    global part

    part = newObj
