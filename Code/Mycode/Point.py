from GlobalValuesLib import *
import math

class Point :
    # init the point
    def __init__(self,x,y) :
        self.x = Decimal(x)
        self.y = Decimal(y)
        self.coordinates = (self.x,self.y)

    # check for equality between 2 points within permissible limits of floating point error
    def __eq__(self,other) :
        if abs(self.x - other.x) <= EPS and abs(self.y - other.y) <= EPS :
            return True
        return False

    # mid point between self and the other point
    def midpoint(self,other) :
        return Point((self.x+other.x)/2,(self.y+other.y)/2)

    # distance of the self from the other point
    def distance(self,other) :
        return Decimal( math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2) )

    # rotate the argument by point by argument theta in clock wise direction
    def rotate(self,theta,other) :
        # translate to shift origin to the point about which rotation has to take place
        other.x -= self.x
        other.y -= self.y

        # perform rotation about origin
        ans = Point( other.x*Decimal( math.cos(theta) ) - other.y*Decimal( math.sin(theta) ),
                     other.x*Decimal( math.sin(theta) ) + other.y*Decimal( math.cos(theta) ) )

        # translate back to restore origin
        ans.x += self.x
        ans.y += self.y
        return ans
    def printme(self) :
        print "Point is ",float(self.x),float(self.y)
