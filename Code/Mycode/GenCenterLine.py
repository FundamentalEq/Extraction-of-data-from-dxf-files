# import sympy
# from sympy.geometry import *

# from sympy import *
from sympy.geometry import *

from GenOutput import *

def FindCenterLine(ls1,ls2) :
    # print ls1 , ls2
    if not ls1.is_parallel(ls2) :
        print "Lines are not parallel thus Center Line cannot be genrated"
        return None

    mid1 = mid2 = None
    x2,y2 = ls2.points
    # for case 1,case 3 and case 4
    if ls1.contains(ls1.projection(x2)) :
        mid1 = x2.midpoint(ls1.projection(x2))

    if ls1.contains(ls1.projection(y2)) :
        if not mid1 :
            mid1 = y2.midpoint(ls1.projection(y2))
        elif not ( mid1 == y2.midpoint(ls1.projection(y2)) ) :
            mid2 = y2.midpoint(ls1.projection(y2))

    x1,y1 = ls1.points
    if ls2.contains(ls2.projection(y1)) :
        if not mid1 :
            mid1 = y1.midpoint(ls2.projection(y1))
        elif not ( mid1 == y1.midpoint(ls2.projection(y1)) ) :
            mid2 = y1.midpoint(ls2.projection(y1))
    if ls2.contains(ls2.projection(x1)) :
        if not mid1 :
            mid1 = x1.midpoint(ls2.projection(x1))
        elif not ( mid1 == x1.midpoint(ls2.projection(x1)) ) :
            mid2 = x1.midpoint(ls2.projection(x1))

    if (not mid1) or (not mid2) :
        print "Error : unable to form centeral line"
        return None
    s = Segment(mid1,mid2)
    return s

def SplitLineSegmetOverPoints(ls1,a,b) :
    c,d = ls1.points
    temp = []

    if a == c :
        if b.distance(d) > 0 :
            temp.append(Segment(b,d))
    elif a == d :
        if b.distance(c) > 0 :
            temp.append(Segment(b,c))
    elif b == c:
        if a.distance(d) > 0 :
            temp.append(Segment(a,d))
    elif b == d:
        if a.distance(c) > 0 :
            temp.append(Segment(a,c))
    else :
        if c.distance(a) < c.distance(b) :
            cc = a
        else :
            cc = b

        if c.distance(cc) > 0 :
            temp.append(Segment(c,cc))

        if d.distance(a) < d.distance(b) :
            dd = a
        else :
            dd = b

        if d.distance(dd) > 0 :
            temp.append(Segment(d,dd))
    return temp

def SplitOverlappingLineSegmets(ls1,ls2,i) :
    # a,b = ls1.points
    # c,d = ls2.points
    # temp = []
    # # case1
    # if ls1.contains(ls1.projection(c)) and ls1.contains(ls1.projection(d)) :
    #     Nls1 = Segment(ls1.contains(ls1.projection(c),ls1.contains(ls1.projection(d))))
    #     Nls2 = ls2
    #
    # # case 2
    # elif ls2.contains(ls2.projection(a)) and ls2.contains(ls2.projection(b)) :
    #     Nls1 = ls1
    #     Nls2 = Segment(ls2.contains(ls2.projection(a),ls2.contains(ls2.projection(b))))
    #
    # # case3
    # elif
    centerline = FindCenterLine(ls1,ls2)
    # print "Centerline" , centerline
    temp = []
    cl1,cl2 = centerline.points
    for t in SplitLineSegmetOverPoints(ls1,ls1.projection(cl1),ls1.projection(cl2)) :
        temp.append(t)
    for t in SplitLineSegmetOverPoints(ls2,ls2.projection(cl1),ls2.projection(cl2)) :
        temp.append(t)
    Nls1 = Segment(ls1.projection(cl1),ls1.projection(cl2))
    Nls2 = Segment(ls2.projection(cl1),ls2.projection(cl2))
    name = "temp" + str(i) + ".shp"
    name2 = "temp" + str(i) + "original.shp"
    MakeShapeFile([ls1,ls2],name2)
    temp2 = []
    for t in temp :
        temp2.append(t)
    temp2.append(Nls1)
    temp2.append(Nls2)
    temp2.append(centerline)
    MakeShapeFile(temp2,name)
    return Nls1,Nls2,centerline,temp
