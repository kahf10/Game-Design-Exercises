# transform (3d wireframe engine) homework
# CS 314, Denison University

from graphics import *
from time import *
from random import *
import math

# Constants #
pixHeight = 400    # height of screen in pixels
pixWidth = 400     # width of screen in pixels
d = 1.0            # distance of eye from screen in world units
screenWidth = 1.0  # width of screen in world size
screenHeight = 1.0 # height of screen in world size 

def projectX(x, z):
    ''' maps x to screen x location '''
    return pixWidth / 2 + (pixWidth / screenWidth) * x * d / (z + d)

def projectY(y, z):
    ''' maps y to screen y location '''
    return pixHeight / 2 + (pixHeight / screenHeight) * y * d / (z + d)


def depth(polygon):
    ''' the average depth of a polygon, represented as a list of points '''
    return sum([point[2] for point in polygon])/len(polygon) # average of z-coordinate

def forward(point, distance):
    ''' update point when player moves forward given distance '''
    point[2] = point[2] - distance

def backward(point, distance):
    ''' update point when player moves backward given distance '''
    point[2] = point[2] + distance
    
def rotate(point, angle, center):
    ''' rotates the polygon 'angle' radians around the point 'center'
    point: a 3D point represented by a list of size 3
    angle: an angle in radians
    center: the point around which we are rotating the point
    '''
    
    # center point on rotation center
    point[0] = point[0] - center[0]
    point[1] = point[1] - center[1]
    point[2] = point[2] - center[2]

     # use the rotation formula
    point[0] = (point[0] * math.cos(angle)) + (point[2] * math.sin(angle))
    point[2] = (point[2] * math.cos(angle)) - (point[0] * math.sin(angle))
   
        
    # un-center point on rotation center
    point[0] = point[0] + center[0]
    point[1] = point[1] + center[1]
    point[2] = point[2] + center[2]

def main():
    ''' Main program that runs everything '''

    win = GraphWin("Projection", pixHeight, pixWidth)

    # create points on a cube
    points = [[-1, 1, 5], [1, 1, 5], [1, -1, 5], [-1, -1, 5], \
              [-1, 1, 7], [1, 1, 7], [1, -1, 7], [-1, -1, 7]]
    
    # create the polygons
    polygons = [(points[0], points[1], points[2], points[3]), \
                (points[4], points[5], points[6], points[7]), \
                (points[0], points[1], points[5], points[4]), \
                (points[2], points[3], points[7], points[6]), \
                (points[0], points[3], points[7], points[4]), \
                (points[1], points[2], points[6], points[5])]

    # sort by z-coordinate, big to small
    polygons = sorted(polygons, key=lambda polygon: -depth(polygon)) 

    while True:
        # draw the polygons
        for poly in polygons:
            # assumes that each polygon has 4 sides
            p1 = poly[0]
            p2 = poly[1]
            p3 = poly[2]
            p4 = poly[3]
            
            polygon = Polygon(Point(projectX(p1[0], p1[2]), projectY(p1[1], p1[2])), Point(projectX(p2[0], p2[2]), projectY(p2[1], p2[2])), Point(projectX(p3[0], p3[2]), projectY(p3[1], p3[2])), Point(projectX(p4[0], p4[2]), projectY(p4[1], p4[2])))
            polygon.draw(win)
        
        # draw buttons
        left = Rectangle(Point(10, 50), Point(20, 60))
        left.draw(win)
        up = Rectangle(Point(30, 30), Point(40, 40))
        up.draw(win)
        right = Rectangle(Point(50, 50), Point(60, 60))
        right.draw(win)
        down = Rectangle(Point(30, 70), Point(40, 80))
        down.draw(win)
        
        click = win.getMouse()
        x = click.getX()
        y = click.getY()

        # make the appropriate transformation
        if 30 <= x <= 40 and 30 <= y <= 40:
            for poly in polygons:
                for point in poly:
                    forward(point, .1)
        elif 30 <= x <= 40 and 70 <= y <= 80:
            for poly in polygons:
                for point in poly:
                    backward(point, .1)
        elif 10 <= x <= 20 and 50 <= y <= 60:
            for poly in polygons:
                for point in poly:
                    rotate(point, 0.0314, [0, 0, -1])
        elif 50 <= x <= 60 and 50 <= y <= 60:
            for poly in polygons:
                for point in poly:
                    rotate(point, -0.0314, [0, 0, -1])

        # erase everything by drawing a big white box!
        clear = Rectangle(Point(0, 0), Point(pixWidth, pixHeight))
        clear.setFill("white")
        clear.draw(win)
            
            
    # close the graphics window
    win.close()

if __name__ == "__main__":
    main()
