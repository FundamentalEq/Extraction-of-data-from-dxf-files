# Python library to interact with dxf files
import ezdxf

# for taking in the file name as argument
import sys

from LineGeometry import *
from GlobalValues import *
from GenCenterLine import *
from GenOutput import *

# Function to check is line-segment1(ls1) and line-segment2(ls2) can form a wall pair
def CanFormWallPair(ls1,ls2) :
    if not ls1.is_parallel(ls2) :
        # print "Failed at parallel"
        return False
    if ls1.facinglength(ls2) < min_wall_width :
        # print "Failed at proj"
        return False
    PrependicularDistance = ls1.prependiculardistance(ls2)
    if PrependicularDistance < min_wall_width :
        return False
    if PrependicularDistance > max_wall_width :
        return False

    # ls1.printme()
    # ls2.printme()
    # print "facing length is ",ls1.facinglength(ls2)
    return True

# The main function that takes input of a dxf file and Extracts the center line
def main() :
    argument = sys.argv
    if not (len(argument)==2) :
        print "Usage: python ExtractLine.py Filename"
        sys.exit()
    FileName = argument[1]

    # Opening the dxf file using ezdxf
    dwg = ezdxf.readfile(FileName)
    modelspace = dwg.modelspace()

    # Extarction of lines-segments from the dxf file and storing them as
    # Segment for further computation
    ElineSegments = []
    for l in modelspace.query('LINE') :
        x1,y1,z1 = l.dxf.start
        x2,y2,z2 = l.dxf.end
        ElineSegments.append(Segment(Point(x1,y1),Point(x2,y2)))

    PrintLines(ElineSegments)
    MakeShapeFile(ElineSegments,"Eline_new.shp")

    # For Storing wether the current line has already been paired or not
    Edone = [ False for i in range(len(ElineSegments)) ]

    # Store the genrated Centerlines
    CenterLines = []

    # Store the number of the centerline associated with the current line
    AssoCenterLine = [-1 for i in range(len(ElineSegments))]

    # Store the pair of wall line,associated with the ith center-line
    AssoEline = []

    ElineSegmetsLen = len(ElineSegments)
    i = 0
    while i < ElineSegmetsLen :
        # print "i : ", i ,ElineSegments[i]
        if not Edone[i] :
            PairIndex = -1
            # print "For ,i = ",i
            # Find the pair index
            j = i + 1
            while j < ElineSegmetsLen :
                if not Edone[j] :
                    # print "     trying j = ",j
                    if CanFormWallPair(ElineSegments[i],ElineSegments[j])  :
                        if PairIndex == -1 :
                            PairIndex = j
                            # break
                        elif ElineSegments[i].facinglength(ElineSegments[j]) > ElineSegments[i].facinglength(ElineSegments[PairIndex]) :
                            PairIndex = j

                j += 1

            print i," ==== ",PairIndex
            # if the PairIndex has been found
            if PairIndex >= 0 :
                # Mark that both the ith and PairIndex th line have been paired
                # and thus cannot be pairred with any other line
                Edone[i] = Edone[PairIndex] = True
                AssoCenterLine[i] = AssoCenterLine[PairIndex] = len(AssoEline)
                AssoEline.append((i,PairIndex))

                ElineSegments[i],ElineSegments[PairIndex],centerline,temp = SplitOverlappingLineSegmets(ElineSegments[i],ElineSegments[PairIndex])
                CenterLines.append(centerline)

                # Add new lines segments genrated due to splitting
                for t in temp :
                    ElineSegments.append(t)

                # Extend the others array also accomodate the new lines
                while len(ElineSegments) > len(Edone) :
                    Edone.append(False)
                    AssoCenterLine.append(-1)

                ElineSegmetsLen = len(ElineSegments)
        i += 1
    PrintLines(ElineSegments)
    # MakeShapeFile(ElineSegments,"ss.shp")
    # print AssoCenterLine

    print "CenterLine before extension"
    PrintLines(CenterLines)
    # for i in range(len(CenterLines)) :
    #     a,b = CenterLines[i].points
    #     print i , float(a.x) ,float(a.y) ,float(b.x) ,float(b.y)
    #     x,y = AssoEline[i]
    #     print "Asso line is x :" ,x
    #     ElineSegments[x].printme()
    #     print "Asso line is y :" ,y
    #     ElineSegments[y].printme()

    Name = FileName.split('.dxf')[0] + "_centerlines_before_extension.shp"
    MakeShapeFile(CenterLines,Name)


    # for extension of center Lines
    for i in range(len(ElineSegments)) :
        for j in range(i+1,len(ElineSegments)) :
            if (AssoCenterLine[i]>-1) and (AssoCenterLine[j] > -1) and ElineSegments[i].intersection(ElineSegments[j])  :
                CenterLines[AssoCenterLine[i]],CenterLines[AssoCenterLine[j]] = JoinCenterLine(CenterLines[AssoCenterLine[i]],CenterLines[AssoCenterLine[j]])

    print "CenterLine after extension"
    PrintLines(CenterLines)
    # writing into a shape file
    Name = FileName.split('.dxf')[0] + "_centerlines_after_extension.shp"
    MakeShapeFile(CenterLines,Name)

    SegmentedCL = [ [] for i in range(len(CenterLines))]

    # Add the original EndPoints
    for i in range(len(CenterLines)) :
        SegmentedCL[i].append(CenterLines[i].points[0])
        SegmentedCL[i].append(CenterLines[i].points[1])

    # Find all the required Segmented Points
    for i in range(len(CenterLines)) :
        for j in range(i+1,len(CenterLines)) :
            # Check if the 2 lines intersect
            if CenterLines[i].intersection(CenterLines[j]) :
                # print i , "intersects with ",j
                p = CenterLines[i].extendedintersection(CenterLines[j])
                SegmentedCL[i].append(p)
                SegmentedCL[j].append(p)



    # Sort all the segmented points in order of their distance to the leftmost
    # and bottom most point

    for i in range(len(SegmentedCL)) :
        # print "line ",i," will be split into ",len(SegmentedCL[i])
        ReferencePoint = SegmentedCL[i][0]

        def SortAlongLine(p1,p2) :
            if ReferencePoint.distance(p1) < ReferencePoint.distance(p2) :
                return -1
            if ReferencePoint.distance(p1) > ReferencePoint.distance(p2) :
                return 1
            if ReferencePoint.distance(p1) == ReferencePoint.distance(p2) :
                return 0

        SegmentedCL[i] = sorted(SegmentedCL[i],SortAlongLine)
        # print "Segment ",i
        # for j in range(len(SegmentedCL[i])) :
        #     SegmentedCL[i][j].printme()
    # check for redundant points and make the new centerlines
    NewCenterLines = []
    for i in range(len(SegmentedCL)) :
        for j in range(len(SegmentedCL[i]) - 1) :
            if not SegmentedCL[i][j] == SegmentedCL[i][j+1] :
                NewCenterLines.append(Segment(SegmentedCL[i][j],SegmentedCL[i][j+1]))

    print "Segmented CenterLines"
    PrintLines(NewCenterLines)
    # writing into a shape file
    Name = FileName.split('.dxf')[0] + "_segmentedCenterLines.shp"
    MakeShapeFile(NewCenterLines,Name)

main()
