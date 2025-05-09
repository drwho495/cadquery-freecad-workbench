import FreeCAD as App
from build123d import *
import math

def _toQuaternion(roll, pitch, yaw):
    rotation = App.Rotation(App.Vector(0, 0, 1), yaw) \
         * App.Rotation(App.Vector(0, 1, 0), pitch) \
         * App.Rotation(App.Vector(1, 0, 0), roll)
    
    return rotation

class FreeCAD_Sketch:
    def __init__(self, sketchName, plane):
        self.sortedSketchGeom = []
        self.sketchObject = App.ActiveDocument.getObject(sketchName)
        self.sketchObject.MakeInternals = True
        self.plane = plane
        
        if self.sketchObject is not None:
            self.sketchObject.Placement.Base.x = self.plane.origin.X
            self.sketchObject.Placement.Base.y = self.plane.origin.Y
            self.sketchObject.Placement.Base.z = self.plane.origin.Z

            rot = _toQuaternion(
                self.plane.location.orientation.X, 
                self.plane.location.orientation.Y, 
                self.plane.location.orientation.Z
            )

            self.sketchObject.Placement.Rotation = rot
        else:
            raise Exception("Sketch doesn't exist!")
                
    def build(self):
        if self.sketchObject is not None:
            subshapes = self.sketchObject.InternalShape.SubShapes
            currentMode = Mode.ADD
            
            print(subshapes)
            
            with BuildSketch(self.plane) as b123Sketch:
                for subshape in subshapes:
                    print(subshape.Edges[0].Curve.TypeId)
                    
                    if len(subshape.Edges) == 1 and subshape.Edges[0].Curve.TypeId == "Part::GeomCircle":
                        edge = subshape.Edges[0]
                            
                        with Locations((edge.Curve.Location.x, edge.Curve.Location.y)):
                            Circle(edge.Curve.Radius, mode=currentMode)
                            
                            print("circle mode: " + str(currentMode))
                    elif len(subshape.Edges) > 1 and subshape.isClosed():
                        with BuildLine():
                            for edge in subshape.Edges:
                                if edge.Curve.TypeId == "Part::GeomLine":
                                    Line((edge.Vertexes[0].Point.x, edge.Vertexes[0].Point.y), (edge.Vertexes[-1].Point.x, edge.Vertexes[-1].Point.y))
                                elif edge.Curve.TypeId == "Part::GeomCircle":
                                    start = edge.Vertexes[0].Point
                                    end = edge.Vertexes[1].Point

                                    curve = edge.Curve.trim(edge.FirstParameter, edge.LastParameter)
                                    half_length = curve.length() / 2

                                    mid_param = curve.parameterAtDistance(half_length, edge.FirstParameter)
                                    mid_point = curve.value(mid_param)
                                    
                                    ThreePointArc((start[0], start[1]), (mid_point[0], mid_point[1]), (end[0], end[1]))
                        make_face(mode=currentMode)
                    
                    currentMode = Mode.SUBTRACT
            
            return b123Sketch.sketch