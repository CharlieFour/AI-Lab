class Shape:
    def calculate_area(self):
        pass

class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def calculate_area(self):
        return self.length * self.width

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def calculate_area(self):
        import math
        return math.pi * self.radius ** 2
    
class Square(Shape):
    def __init__(self, side):
        self.side = side
    
    def calculate_area(self):
        return self.side ** 2
    
class Cylinder(Shape):
    def __init__(self, radius, height):
        self.radius = radius
        self.height = height
    
    def calculate_area(self):
        import math
        return 2 * math.pi * self.radius * (self.radius + self.height)
    
def main():
    rectangle = Rectangle(5, 3)
    circle = Circle(4)
    square = Square(4)
    cylinder = Cylinder(3, 7)

    print(f"Area of Rectangle: {rectangle.calculate_area()}")
    print(f"Area of Circle: {circle.calculate_area()}")
    print(f"Area of Square: {square.calculate_area()}")
    print(f"Surface Area of Cylinder: {cylinder.calculate_area()}")

main()