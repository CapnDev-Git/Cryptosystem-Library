from typing import Optional


class EllipticCurve:
    """
    Represents an elliptic curve defined over a finite field.

    Attributes:
        a (int): Coefficient 'a' of the elliptic curve equation.
        b (int): Coefficient 'b' of the elliptic curve equation.
        p (int): Prime number defining the finite field.
    """

    def __init__(self, a: int, b: int, p: int):
        """
        Initializes the elliptic curve.

        Args:
            a (int): Coefficient 'a' of the elliptic curve equation.
            b (int): Coefficient 'b' of the elliptic curve equation.
            p (int): Prime number defining the finite field.
        """
        self.a = a
        self.b = b
        self.p = p

    def contains_point(self, x: int, y: int) -> bool:
        """
        Checks if a point (x, y) satisfies the elliptic curve equation.

        Args:
            x (int): x-coordinate of the point.
            y (int): y-coordinate of the point.

        Returns:
            bool: True if the point satisfies the curve equation, False otherwise.
        """
        return (y**2 - x**3 - self.a * x - self.b) % self.p == 0

    def inverse_point(self, point: "EllipticPoint") -> "EllipticPoint":
        """
        Calculates the inverse of a point on the curve.

        Args:
            point (EllipticPoint): The point to find the inverse of.

        Returns:
            EllipticPoint: The inverse of the given point.
        """
        return EllipticPoint(self, point.x, (-point.y) % self.p)

    def add_points(
        self, point1: "EllipticPoint", point2: "EllipticPoint"
    ) -> Optional["EllipticPoint"]:
        """
        Adds two points on the elliptic curve.

        Args:
            point1 (EllipticPoint): The first point to add.
            point2 (EllipticPoint): The second point to add.

        Returns:
            EllipticPoint or None: The result of the addition, or None if the operation results in the point at infinity.
        """
        if point1 == point2:
            if point1.y == 0:
                return None
            slope = (3 * point1.x**2 + self.a) * pow(2 * point1.y, -1, self.p)
        else:
            if point1.x == point2.x:
                return None
            slope = (point2.y - point1.y) * pow(point2.x - point1.x, -1, self.p)
        x = (slope**2 - point1.x - point2.x) % self.p
        y = (slope * (point1.x - x) - point1.y) % self.p
        return EllipticPoint(self, x, y)

    def multiply_point(self, point: "EllipticPoint", scalar: int) -> "EllipticPoint":
        """
        Performs scalar multiplication of a point on the elliptic curve.

        Args:
            point (EllipticPoint): The point to multiply.
            scalar (int): The scalar value by which to multiply the point.

        Returns:
            EllipticPoint: The result of the scalar multiplication.
        """
        result = None
        for _ in range(scalar):
            if result is None:
                result = point
            else:
                result = self.add_points(result, point)
        return result


class EllipticPoint:
    """
    Represents a point on an elliptic curve.

    Attributes:
        curve (EllipticCurve): The elliptic curve to which the point belongs.
        x (int): The x-coordinate of the point.
        y (int): The y-coordinate of the point.
    """

    def __init__(self, curve: EllipticCurve, x: int, y: int):
        """
        Initializes the elliptic point.

        Args:
            curve (EllipticCurve): The elliptic curve to which the point belongs.
            x (int): The x-coordinate of the point.
            y (int): The y-coordinate of the point.
        """
        self.curve = curve
        self.x = x
        self.y = y

        assert curve.contains_point(x, y)

    def __eq__(self, other: "EllipticPoint") -> bool:
        """
        Checks if two elliptic points are equal.

        Args:
            other (EllipticPoint): The other point to compare with.

        Returns:
            bool: True if the points are equal, False otherwise.
        """
        return self.curve == other.curve and self.x == other.x and self.y == other.y

    def __add__(self, other: "EllipticPoint") -> Optional["EllipticPoint"]:
        """
        Adds two elliptic points.

        Args:
            other (EllipticPoint): The other point to add.

        Returns:
            EllipticPoint or None: The result of the addition, or None if the operation results in the point at infinity.
        """
        return self.curve.add_points(self, other)

    def __mul__(self, scalar: int) -> "EllipticPoint":
        """
        Performs scalar multiplication of an elliptic point.

        Args:
            scalar (int): The scalar value by which to multiply the point.

        Returns:
            EllipticPoint: The result of the scalar multiplication.
        """
        return self.curve.multiply_point(self, scalar)

    def __str__(self) -> str:
        """
        Returns a string representation of the elliptic point.

        Returns:
            str: A string representation of the point.
        """
        return f"({self.x}, {self.y})"
