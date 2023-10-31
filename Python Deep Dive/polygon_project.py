import math


class Polygon:

    def __init__(self,n, R) -> None:
        self._n = n
        self._R = R

    def __repr__(self) -> str:
        return f"Polygon(n={self._n}, R={self._R})"

    
    @property
    def count_vertices(self):
        return self._n

    @property
    def count_edges(self):
        return self._n

    @property
    def circum_radius(self):
        return self._R

    @property
    def interior_angle(self):
        return (self._n -2 ) * 180/self._n

    @property
    def side_length(self):
        return 2 * self._R * math.sin(math.pi /self._n)

    @property
    def apothem(self):
        return  self._R * math.cos(math.pi /self._n)

    @property
    def area(self):
        return  (self._n/ 2) * self.side_length * self.apothem

    @property
    def perimeter(self):
        return self._n * self.side_length


def test_polygon():
    n=3
    R=1
    p=Polygon(n,R)
    assert str(p) == f"Polygon(n={n}, R={R})", f"actual: {str(p)}"
        
if __name__ == "__main__":
    test_polygon()
