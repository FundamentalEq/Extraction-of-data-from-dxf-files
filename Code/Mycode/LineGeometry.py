#Python library for geometry and mathematical computations
from LineSegment import *

# importing for ThersholdMax
from GlobalValues import *
# there can be 4 valid cases as follows :



# Function to extend the line segment ls1 to point p
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
    # If the 2 line segments are parallel
    if ls1.is_parallel(ls2) :
        return ls1,ls2
    # print "Join centerline called"
    #Find the point of intersection of the lines
    IntersectionPoint = ls1.extendedintersection(ls2)
    if not IntersectionPoint :
        ls1.printme()
        print ls1.angle
        ls2.printme()
        print ls2.angle
        raise Exception('Disastour')
    #Extend both the line segments to the point of intesection
    ls1 = ExtendLineSegment(ls1,IntersectionPoint)
    ls2 = ExtendLineSegment(ls2,IntersectionPoint)
    return ls1,ls2
