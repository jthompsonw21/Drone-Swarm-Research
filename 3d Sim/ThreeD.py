#Similar to TwoD but with 3 dimensions

class ThreeD:

    def __init__(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __repr__(self):
        return 'ThreeD(%s, %s, %s)' % (self.x, self.y, self.z)

    def __add__(self, other):
        return ThreeD(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return ThreeD(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        return ThreeD(self.x * other, self.y * other, self.z * other)

    def __truediv__(self, other):
        return ThreeD(self.x / other, self.y / other, self.z / other)

    def __floordiv__(self,other):
        return Threed(self.x // other, self.y //other, self.z // other)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return self

    def __idiv__(self, other):
        self.x /= other
        self.y /= other
        self.z /= other
        return self

    def __imul__(self, other):
        self.x *= other
        self.y *= other
        self.z *= other
        return self



    def __ifloordiv__(self,other):
        self.x //= other
        self.y //= other
        self.z //= other
        return self

    def __iter__(self):
        yield self.x 
        yield self.y 
        yield self.z

    def mag(self):
        return ((self.x ** 2) + (self.y ** 2) + (self.z ** 2)) ** 0.5

    def xymag(self):
        return ((self.x ** 2) + (self.y ** 2)) ** 0.5

    def toUnitVector(self):
        return ThreeD((self.x/self.mag()), (self.y/self.mag()), (self.z/self.mag()))

    def dot(self, other):
        return (self.x * other.x) + (self.y * other.y) + (self.z * other.z)
    
    def cross(self, other):
        return ThreeD(((self.y*other.z)-(self.z*other.y)), ((self.z*other.x)-(self.x*other.z)), ((self.x*other.y)-(self.y*other.x)))

