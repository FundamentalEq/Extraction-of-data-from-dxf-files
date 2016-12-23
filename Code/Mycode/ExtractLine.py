# Python library to interact with dxf files
import ezdxf
#Python library for geometry and mathematical computations
# import sympy
# from sympy.geometry import *

# for writing into a shape file
from osgeo import ogr

#for checking and deleting the file
import os

from LineGeometry import *
from GlobalValues import *
from GenCenterLine import *


def CanFormWallPair(ls1,ls2) :
    if not ls1.is_parallel(ls2) :
        return False
    if FindProjectedLen(ls1,ls2) == 0.0 :
        return False
    PrependicularDistance = FindPrependicularDistance(ls1,ls2)
    if PrependicularDistance < min_wall_width :
        return False
    if PrependicularDistance > max_wall_width :
        return False
    return True

def ExtendLineSegment(ls1,p) :
    a,b = ls1.points
    s = ls1

    #if the point already lies on the line-segment the nothing needs to be done
    if not s.contains(p) :
        #else find the end point of the line segment  nearer to the point "p"
        #and replace it with the point "p"
        if a.distance(p) < b.distance(p) :
            s = Segment(p,b)
        else :
            s = Segment(a,p)
    return s

def JoinCenterLine(ls1,ls2) :
    #Find the lines corressponding to line segments
    l1 = Line(ls1)
    l2 = Line(ls2)

    #Find the point of intersection of the lines
    IntersectionPointArray = l1.intersection(l2)
    IntersectionPoint = IntersectionPointArray[0]

    #Extend both the line segments to the point of intesection
    ls1 = ExtendLineSegment(ls1,IntersectionPoint)
    ls2 = ExtendLineSegment(ls2,IntersectionPoint)
    return ls1,ls2

def create_line(ls) :
    a,b = ls.points
    line = ogr.Geometry(ogr.wkbLineString)
    line.AddPoint(float(a.x), float(a.y))
    line.AddPoint(float(b.x), float(b.y))
    return line

def MakeShapeFile(ArrayOfLineSegmets,name) :
    print "Going to create the impossible"
    driver = ogr.GetDriverByName('ESRI Shapefile')
    shapefile_name = name
    if os.path.exists(shapefile_name):
        os.remove(shapefile_name)
    out_data_source = driver.CreateDataSource(shapefile_name)

    # Create Layer

    out_layer = out_data_source.CreateLayer('center_line', geom_type=ogr.wkbLineString)

    # Set Geometry

    out_layer_defn = out_layer.GetLayerDefn()
    for i in range(len(ArrayOfLineSegmets)) :
        new_geom = create_line(ArrayOfLineSegmets[i])
        feature = ogr.Feature(out_layer_defn)
        feature.SetGeometry(new_geom)
        out_layer.CreateFeature(feature)
        feature.Destroy()

    out_data_source.Destroy()
def PrintLines(Array) :
    for i in range(len(Array)) :
        a,b = Array[i].points
        print i , float(a.x) ,float(a.y) ,float(b.x) ,float(b.y)

def main() :
    dwg = ezdxf.readfile("1RoomWSSNew.dxf")
    modelspace = dwg.modelspace()
    # Extarction of lines-segments from the dxf file and storing them as
    # sympy.geometry.Segment for further computation
    ElineSegments = []
    for l in modelspace.query('LINE') :
        x1,y1,z1 = l.dxf.start
        x2,y2,z2 = l.dxf.end
        ElineSegments.append(Segment(Point(x1,y1),Point(x2,y2)))

    PrintLines(ElineSegments)
    MakeShapeFile(ElineSegments,"Eline.shp")
    # For Storing wether the current line has already been paired or not
    Edone = [ False for i in range(len(ElineSegments)) ]

    CenterLines = []
    AssoCenterLine = [-1 for i in range(len(ElineSegments))]
    AssoEline = []
    for i in range(len(ElineSegments)) :
        if not Edone[i] :
            PairIndex = -1

            # Find the pair index
            for j in range(i+1,len(ElineSegments)) :
                if not Edone[j] :
                    if CanFormWallPair(ElineSegments[i],ElineSegments[j])  :
                        if PairIndex == -1 :
                            PairIndex = j
                        elif FindProjectedLen(ElineSegments[i],ElineSegments[j]) > FindProjectedLen(ElineSegments[i],ElineSegments[PairIndex]) :
                            PairIndex = j

            # if the PairIndex has been found
            if PairIndex >= 0 :
                Edone[i] = Edone[PairIndex] = True
                AssoCenterLine[i] = AssoCenterLine[PairIndex] = len(AssoEline)
                AssoEline.append((i,PairIndex))

    print AssoCenterLine
    for i,j in AssoEline :
        CenterLines.append(FindCenterLine(ElineSegments[i],ElineSegments[j]))

    PrintLines(CenterLines)
    MakeShapeFile(CenterLines,"cv1.shp")


    # for extension of center Lines
    for i in range(len(ElineSegments)) :
        for j in range(i+1,len(ElineSegments)) :
            if (AssoCenterLine[i]>-1) and (AssoCenterLine[j] > -1) and (len(ElineSegments[i].intersection(ElineSegments[j])) > 0) :
                CenterLines[AssoCenterLine[i]],CenterLines[AssoCenterLine[j]] = JoinCenterLine(CenterLines[AssoCenterLine[i]],CenterLines[AssoCenterLine[j]])

    for i in range(len(CenterLines)) :
        a,b = CenterLines[i].points
        print i , float(a.x) ,float(a.y) ,float(b.x) ,float(b.y)

    # writing into a shape file
    MakeShapeFile(CenterLines,"CenterLine.shp")

main()
