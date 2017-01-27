from LineSegment import *
s = Segment(Point(1,1),Point(1,2))
s2 = Segment(Point(0,1.5),Point(2,1.5))
s.extendedintersection(s2).printme()
print "ans should be 1 ,1.5"

s = Segment(Point(1,1),Point(2,2))
s2 = Segment(Point(-1,1),Point(0,0))
s.extendedintersection(s2).printme()
print "ans should be 0 ,0"

s = Segment(Point(0,0),Point(1,-1))
s2 = Segment(Point(0,-1),Point(1,0))
s.extendedintersection(s2).printme()
print "ans should be 0.5 ,-0.5"


s = Segment(Point(1,0),Point(2,0))
s2 = Segment(Point(3,4),Point(3,-4))
s.extendedintersection(s2).printme()
print "ans should be 3 ,0"
