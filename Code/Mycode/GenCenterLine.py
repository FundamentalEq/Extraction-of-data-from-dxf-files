# from sympy import *
from sympy.geometry import *

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
