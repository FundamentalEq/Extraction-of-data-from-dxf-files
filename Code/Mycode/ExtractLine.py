# Python library to interact with dxf files
import ezdxf
#Python library for geometry and mathematical computations
import sympy
import sympy.geometry

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

def main() :
    dwg = ezdxf.readfile("1RoomWSS.dxf")
    modelspace = dwg.modelspace()
    # Extarction of lines-segments from the dxf file and storing them as
    # sympy.geometry.Segment for further computation
    ElineSegments = []
    for l in modelspace.query('LINE') :
        x1,y1,z1 = l.dxf.start
        x2,y2,z2 = l.dxf.end
        ElineSegments.append(Segment(Point(x1,y1),Point(x2,y2)))

    print ElineSegments
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
    print CenterLines
    
    # for extension of center Lines
    for i in range(len(ElineSegments)) :
        for j in range(i+1,len(ElineSegments)) :
            if len(ElineSegments[i].intersection(ElineSegments[j])) > 0 :
                CenterLines[AssoCenterLine[i]],CenterLines[AssoCenterLine[j]] = JoinCenterLine(CenterLines[AssoCenterLine[i]],CenterLines[AssoCenterLine[j]])

    print CenterLines

main()