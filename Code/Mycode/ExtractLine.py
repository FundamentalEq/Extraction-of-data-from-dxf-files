# Python library to interact with dxf files
import ezdxf
#Python library for geometry and mathematical computations

from LineGeometry import *
from GlobalValues import *
from GenCenterLine import *
from GenOutput import *

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

    ElineSegmetsLen = len(ElineSegments)
    i = 0
    while i < ElineSegmetsLen :
        print "i : ", i ,ElineSegments[i]
        if not Edone[i] :
            PairIndex = -1

            # Find the pair index
            j = i + 1
            while j < ElineSegmetsLen :
                if not Edone[j] :
                    if CanFormWallPair(ElineSegments[i],ElineSegments[j])  :
                        if PairIndex == -1 :
                            PairIndex = j
                        elif FindProjectedLen(ElineSegments[i],ElineSegments[j]) > FindProjectedLen(ElineSegments[i],ElineSegments[PairIndex]) :
                            PairIndex = j

                j += 1

            # if the PairIndex has been found
            if PairIndex >= 0 :
                Edone[i] = Edone[PairIndex] = True
                AssoCenterLine[i] = AssoCenterLine[PairIndex] = len(AssoEline)
                AssoEline.append((i,PairIndex))

                ElineSegments[i],ElineSegments[PairIndex],centerline,temp = SplitOverlappingLineSegmets(ElineSegments[i],ElineSegments[PairIndex],i)
                CenterLines.append(centerline)
                for t in temp :
                    ElineSegments.append(t)
                PrintLines(temp)
                while len(ElineSegments) > len(Edone) :
                    Edone.append(False)
                    AssoCenterLine.append(-1)

                ElineSegmetsLen = len(ElineSegments)
        i += 1
    PrintLines(ElineSegments)
    MakeShapeFile(ElineSegments,"ss.shp")
    print AssoCenterLine
    # for i,j in AssoEline :
    #     CenterLines.append(FindCenterLine(ElineSegments[i],ElineSegments[j]))

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
