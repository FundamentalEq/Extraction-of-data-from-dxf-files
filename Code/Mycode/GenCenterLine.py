# import sympy
# from sympy.geometry import *

from sympy import *
from sympy.geometry import *

from LineGeometry import *
from GenOutput import *
from GlobalValues import *
# Function that find the centerline , given 2 line segments ls1 and ls2
# For understanding the working of the function please refer to presentation1
def FindCenterLine(ls1,ls2) :
    # print ls1 , ls2
    if not CheckParallelwithThreshold(ls1,ls2) :
        print "Lines are not parallel thus Center Line cannot be genrated"
        return None

    projectedlen = FindProjectedLen(ls1,ls2)

    if (abs(float(projectedlen) - float(ls1.length)) < min_wall_width) and (abs(float(projectedlen) - float(ls2.length)) < min_wall_width) :
        print "inside new"
        x2,y2 = ls2.points
        mid1 =  x2.midpoint(ls1.projection(x2))
        mid2 =  y2.midpoint(ls1.projection(y2))
        s = Segment(mid1,mid2)
        return s

    mid1 = None
    mid2 = None
    x2,y2 = ls2.points
    if CheckIfLineSegmentContainsPoint(ls1,ls1.projection(x2)) :
        print "did contains"
        mid1 = x2.midpoint(ls1.projection(x2))

    print float(x2.x),float(x2.y)
    print "mid1 = ",mid1
    print "mid2 = ",mid2

    if CheckIfLineSegmentContainsPoint(ls1,ls1.projection(y2)) :
        if not mid1 :
            mid1 = y2.midpoint(ls1.projection(y2))
        elif (not mid1 == y2.midpoint(ls1.projection(y2))) and (not mid2)  :
            mid2 = y2.midpoint(ls1.projection(y2))

    print float(y2.x),float(y2.y)
    print "mid1 = ",mid1
    print "mid2 = ",mid2

    x1,y1 = ls1.points
    if CheckIfLineSegmentContainsPoint(ls2,ls2.projection(y1)) :
        if not mid1 :
            mid1 = y1.midpoint(ls2.projection(y1))
        elif  (not mid1 == y1.midpoint(ls2.projection(y1))) and (not mid2) :
            mid2 = y1.midpoint(ls2.projection(y1))

    print float(y1.x),float(y1.y)
    print "mid1 = ",mid1
    print "mid2 = ",mid2

    if CheckIfLineSegmentContainsPoint(ls2,ls2.projection(x1)) :
        if not mid1 :
            mid1 = x1.midpoint(ls2.projection(x1))
        elif (not mid1 == x1.midpoint(ls2.projection(x1)))  and (not mid2) :
            mid2 = x1.midpoint(ls2.projection(x1))

    print float(x1.x),float(x1.y)
    print "mid1 = ",mid1
    print "mid2 = ",mid2

    if (not mid1) or (not mid2) :
        print "Error : unable to form centeral line" ,float(projectedlen)
        if  mid1 :
            mid2 = mid1
        elif mid2 :
            mid1 = mid2
        # return None
    s = Segment(mid1,mid2)
    return s

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
    if float(a.distance(c)) < EPS :
        if float(b.distance(d)) > min_wall_width :
            temp.append(Segment(b,d))
    elif float(a.distance(d)) < EPS :
        if float(b.distance(c)) > min_wall_width :
            temp.append(Segment(b,c))
    elif float(b.distance(c)) < EPS :
        if float(a.distance(d)) > min_wall_width :
            temp.append(Segment(a,d))
    elif float(b.distance(d)) < EPS:
        if float(a.distance(c)) > min_wall_width :
            temp.append(Segment(a,c))
    # case 1,2
    else :
        if c.distance(a) < c.distance(b) :
            cc = a
        else :
            cc = b

        if c.distance(cc) > min_wall_width :
            temp.append(Segment(c,cc))

        if d.distance(a) < d.distance(b) :
            dd = a
        else :
            dd = b

        if d.distance(dd) > min_wall_width :
            temp.append(Segment(d,dd))
    return temp

# Function extract the centerline, and split the line segments , into the part used for genration of centerline
# and the part not used for the genration of the center line
def SplitOverlappingLineSegmets(ls1,ls2) :
    centerline = FindCenterLine(ls1,ls2)
    # print "Centerline" , centerline
    temp = []
    cl1,cl2 = centerline.points
    for t in SplitLineSegmetOverPoints(ls1,ls1.projection(cl1),ls1.projection(cl2)) :
        if float(t.length) > min_wall_width :
            print "t = ",float(t.length)
            temp.append(t)
    for t in SplitLineSegmetOverPoints(ls2,ls2.projection(cl1),ls2.projection(cl2)) :
        if float(t.length) > min_wall_width :
            print "t = ", float(t.length)
            temp.append(t)
    Nls1 = Segment(ls1.projection(cl1),ls1.projection(cl2))
    Nls2 = Segment(ls2.projection(cl1),ls2.projection(cl2))
    return Nls1,Nls2,centerline,temp
