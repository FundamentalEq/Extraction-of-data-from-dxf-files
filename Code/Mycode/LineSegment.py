from decimal import *
from Point import Point
import math

from GlobalValuesLib import *

class Segment:

    Origin = Point(0,0)

    def __init__(self,a,b) :

        if a == b :
            raise Exception('Single point cannot form a line segment')
        # if the line is vertical
        if abs(a.x - b.x) <= EPS :
            if a.y < b.y :
                self.a = a
                self.b = b
            else :
                self.a = b
                self.b = a

        else :
             if a.x < b.x :
                 self.a = a
                 self.b = b
             else :
                 self.a = b
                 self.b = a

        self.length = a.distance(b)
        self.coordinates = (self.a,self.b)
        self.points = (self.a,self.b)

        # finding slope of the line
        if abs(b.x - a.x) <= EPS :
            self.slope = Inf
        else :
            self.slope = (b.y - a.y)/(b.x - a.x)

        self.angle = math.atan2(self.b.y - self.a.y,self.b.x - self.a.x)

    # Check if the two line segments ar
    def is_parallel(self,ls) :
        diff = abs(self.angle - ls.angle)
        if diff < RadianEPS :
            return True
        if abs(diff - math.pi) < RadianEPS :
            return True
        return False

    # Check if the line segment contains the given point "p" or not
    def contains(self,p) :
        # if p is same as self.a or self.b
        if p.distance(self.a) <= EPS or p.distance(self.b) <= EPS :
            return True
        if self.is_parallel(Segment(p,self.a)) :
            # if the line is vertical
            if abs(self.a.x - self.b.x) <= EPS :
                if self.a.y <= p.y and p.y <= self.b.y :
                    return True
            elif self.a.x <= p.x and p.x <= self.b.x :
                return True
        return False

    # find the projection of the given point "p" on the line segment , also to
    # find the projection of the line segment on the line segment
    def projection(self,p) :

        # if the incoming p is a LineSegment
        if isinstance(p,Segment) :
            return Segment(self.projection(p.a),self.projection(p.b))

        # if the point is same as a
        if p == self.a :
            return self.a
        # if the point is same as b
        if p == self.b :
            return self.b

        # if the point itself lies on the line segment return the point
        if self.is_parallel(Segment(self.a,p)) :
            return p

        # shift self.Origin to a
        bn = Point(self.b.x - self.a.x,self.b.y - self.a.y)
        pn = Point(p.x - self.a.x ,p.y - self.a.y)

        # form the unit vector
        bn = Point(bn.x/self.Origin.distance(bn) , bn.y/self.Origin.distance(bn))

        # find dot product
        t = bn.x * pn.x + bn.y * pn.y

        # find the projected point
        ans = Point(t*bn.x,t*bn.y)

        # translate back the self.Origin
        ans = Point(ans.x + self.a.x,ans.y + self.a.y)

        return ans

    def extendedintersection(self,ls):
        xdiff = (self.b.x - self.a.x,ls.b.x - ls.a.x)
        ydiff = (self.b.y - self.a.y,ls.b.y - ls.a.y)

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)

        if abs(div) <= EPS:
            return None

        d = (det(self.a.coordinates,self.b.coordinates), det(ls.a.coordinates,ls.b.coordinates))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        return Point(-x,-y)

    def intersection(self,ls) :
        p = self.extendedintersection(ls)

        if not p :
            return False

        if self.contains(p) and ls.contains(p) :
            return True

        return False

    # case1
    # A --------------
    # B   ----------

    # case2
    # A     --------------
    # B   ----------------------

    # case3
    # A --------------
    # B   -----------------

    # case4
    # A         --------------
    # B   ----------

    def facinglength(self,ls) :
        # if the 2 LineSegments are not parallel => they will intersect => facing length = 0
        if not self.is_parallel(ls) :
            return Decimal(0)

        # take projection of ls on self
        ls = self.projection(ls)

        # if the lines are exact vertical
        if self.slope == Inf :
            if self.b.y < ls.a.y or ls.b.y < self.a.y :
                return Decimal(0)

            # case 1
            if self.a.y <= ls.a.y and ls.b.y <= self.b.y :
                return ls.length

            # case 2
            if ls.a.y <= self.a.y and self.b.y <= ls.b.y :
                return self.length

            # case 3
            if self.a.y <= ls.a.y  and self.b.y <= ls.b.y :
                return ls.a.distance(self.b)

            # case 4
            if ls.a.y <= self.a.y and ls.b.y <= self.b.y :
                return self.a.distance(ls.b)

            # case facinglength is 0
            return Decimal(0)

        if self.b.x < ls.a.x or ls.b.x < self.a.x :
            return Decimal(0)

        # case 1
        if self.a.x <= ls.a.x and ls.b.x <= self.b.x :
            return ls.length

        # case 2
        if ls.a.x <= self.a.x and self.b.x <= ls.b.x :
            return self.length

        # case 3
        if self.a.x <= ls.a.x  and self.b.x <= ls.b.x :
            return ls.a.distance(self.b)

        # case 4
        if ls.a.x <= self.a.x and ls.b.x <= self.b.x :
            return self.a.distance(ls.b)

        # case facinglength is 0
        return Decimal(0)

    def prependiculardistance(self,ls) :

        # if the incoming is a point
        if isinstance(ls,Point) :
            return ls.distance(self.projection(ls))

        if not self.is_parallel(ls) :
            return Decimal(0)

        # if the incoming is a line segment
        return ls.a.distance(self.projection(ls.a))

    def printme(self) :
        print "Line is ",float(self.a.x),float(self.a.y),float(self.b.x),float(self.b.y)
