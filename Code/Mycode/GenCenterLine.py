from LineSegment import *

from LineGeometry import *
from GenOutput import *
from GlobalValues import *
# Function that find the centerline , given 2 line segments ls1 and ls2
# For understanding the working of the function please refer to presentation1

def FindCenterLine(ls1,ls2) :
    lsn = ls1.projection(ls2)
    # if the lines are exact vertical
    # print "ls1"
    # ls1.printme()
    # print "ls2"
    # ls2.printme()
    # print "lsn"
    # lsn.printme()
    if lsn.slope == Inf :
        # case 1
        if lsn.a.y <= ls1.a.y and ls1.b.y <= lsn.b.y :
            centerline = ls1
        # case 2
        if ls1.a.y <= lsn.a.y and lsn.b.y <= ls1.b.y :
            centerline = lsn
        # case 3
        if lsn.a.y <= ls1.a.y  and lsn.b.y <= ls1.b.y :
            centerline = Segment(ls1.a,lsn.b)
        # case 4
        if ls1.a.y <= lsn.a.y and ls1.b.y <= lsn.b.y :
            centerline = Segment(lsn.a,ls1.b)

    else :
        # case 1
        if lsn.a.x <= ls1.a.x and ls1.b.x <= lsn.b.x :
            centerline = ls1
        # case 2
        if ls1.a.x <= lsn.a.x and lsn.b.x <= ls1.b.x :
            centerline = lsn
        # case 3
        if lsn.a.x <= ls1.a.x  and lsn.b.x <= ls1.b.x :
            centerline = Segment(ls1.a,lsn.b)
        # case 4
        if ls1.a.x <= lsn.a.x and ls1.b.x <= lsn.b.x :
            centerline = Segment(lsn.a,ls1.b)

    if centerline == None :
        raise Exception('centerline not found')

    # print "centerline"
    # centerline.printme()
    centerline2 = ls2.projection(centerline)
    # print "centerline2"
    # centerline2.printme()
    ans = Segment(centerline.a.midpoint(centerline2.a),centerline.b.midpoint(centerline2.b))
    return ans

# Function splits the linse Segment ls1, into parts that don't overlap with the
# Segment formed by points a and b
# there can be 4 valid cases as follows :

# case1
# A --------------
# B   ----------

# case2
# A     --------------
# B   ----------------------

# case3
# A --------------
# B   ------------

# case4
# A  --------------
# B  ----------
def SplitLineSegmetOverPoints(ls1,a,b) :
    c,d = ls1.points
    temp = []
    # Case 3,4
    if a == c :
        if b.distance(d) > EPS :
            temp.append(Segment(b,d))
    elif b == d:
        if a.distance(c) > EPS :
            temp.append(Segment(a,c))
    # case 1,2
    else :
        temp.append(Segment(c,a))
        temp.append(Segment(b,d))
    return temp

# Function extract the centerline, and split the line segments , into the part used for genration of centerline
# and the part not used for the genration of the center line
def SplitOverlappingLineSegmets(ls1,ls2) :
    # print "inside split line segment"
    centerline = FindCenterLine(ls1,ls2)
    # print "Got my centerline"
    centerline.printme()
    # print "Centerline" , centerline
    temp = []
    cl1,cl2 = centerline.points
    for t in SplitLineSegmetOverPoints(ls1,ls1.projection(cl1),ls1.projection(cl2)) :
        if float(t.length) > min_wall_width :
            # print "t = ",float(t.length)
            temp.append(t)
    for t in SplitLineSegmetOverPoints(ls2,ls2.projection(cl1),ls2.projection(cl2)) :
        if float(t.length) > min_wall_width :
            # print "t = ", float(t.length)
            temp.append(t)
    Nls1 = Segment(ls1.projection(cl1),ls1.projection(cl2))
    Nls2 = Segment(ls2.projection(cl1),ls2.projection(cl2))
    return ls1,ls2,centerline,temp
