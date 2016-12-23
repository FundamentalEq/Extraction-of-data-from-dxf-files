from LineGeometry import *

A = Segment(Point(0,0),Point(0,1))
B = Segment(Point(1,0),Point(1,1))

print A.points ,B.points
print FindProjectedLen(A,B)
print FindPrependicularDistance(A,B)

A = Segment(Point(0,0),Point(0,2))
B = Segment(Point(1,0.5),Point(1,1.5))

print A.points ,B.points
print FindProjectedLen(A,B)
print FindPrependicularDistance(A,B)

A = Segment(Point(0,0.5),Point(0,1.5))
B = Segment(Point(1,0),Point(1,2))

print A.points ,B.points
print FindProjectedLen(A,B)
print FindPrependicularDistance(A,B)

A = Segment(Point(0,0),Point(0,1))
B = Segment(Point(1,0.5),Point(1,1.5))

print A.points ,B.points
print FindProjectedLen(A,B)
print FindPrependicularDistance(A,B)


A = Segment(Point(0,0.5),Point(0,1.5))
B = Segment(Point(1,0),Point(1,1))

print A.points ,B.points
print FindProjectedLen(A,B)
print FindPrependicularDistance(A,B)

A = Segment(Point(0,0),Point(0,1))
B = Segment(Point(1,3),Point(1,4))

print A.points ,B.points
print FindProjectedLen(A,B)
print FindPrependicularDistance(A,B)
