from LineSegment import *
s = Segment(Point(1,1),Point(1,2))
a = Point(2,1.5)
b = s.projection(a)
a.printme()
print "B is ",float(b.x)," ",float(b.y)


s = Segment(Point(1,1),Point(2,2))
a = Point(0,0)
a.printme()
b = s.projection(a)
print "B is ",float(b.x)," ",float(b.y)


s = Segment(Point(1,1),Point(2,2))
a = Point(2,0)
a.printme()
b = s.projection(a)
print "B is ",float(b.x)," ",float(b.y)


s = Segment(Point(1,0),Point(2,0))
a = Point(3,4)
a.printme()
b = s.projection(a)
print "B is ",float(b.x)," ",float(b.y)
