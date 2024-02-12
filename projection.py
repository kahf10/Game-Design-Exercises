# Projection homework
# CS 314, Denison University

from graphics import *
from time import *
from random import *

# Constants #
pixHeight = 400    # height of screen in pixels
pixWidth = 400     # width of screen in pixels
d = 1.0            # distance of eye from screen in world units
screenWidth = 1.0  # width of screen in world size
screenHeight = 1.0 # height of screen in world size 

def projectX(x, z):
    ''' maps x to screen x location '''
    return (pixWidth/2) + ((x*d)/(d+z) * (pixWidth/screenWidth))

def projectY(y, z):
    ''' maps y to screen y location '''
    return (pixHeight/2) + ((y*d)/(d+z) * (pixHeight/screenHeight))

def depth(polygon):
    ''' the average depth of a polygon, represented as a list of points '''
    return sum([point[2] for point in polygon])/len(polygon) # average of z-coordinate

def main():
    ''' Main program that runs everything '''

    win = GraphWin("Projection", pixHeight, pixWidth)

    # create points on a cube
    points = []
    points = [(-1, 1, 5), (-1, -1 ,5), (1, -1 ,5), (1, 1, 5), (1, -1, 7), (1, 1, 7), (-1, 1, 7), (-1, -1, 7)]
    # points should be a list of points, represented as lists or tuples of size 3 
    # create a list of points on a cube with opposite corners at (-1, 1, 5) and (1, -1, 7)
    # i.e., points = [(-1, 1, 5), ... other points ... ]


    # create the polygons
    polygons = []
    face1 = [points[0], points[1], points[2], points[3]] #Bottom surface
    face2 = [points[4], points[5], points[6], points[7]] #Top surface
    face3 = [points[0], points[1], points[7], points[6]] #Front surface
    face4 = [points[0], points[6], points[5], points[3]] #Left surface
    face5 = [points[4], points[5], points[3], points[2]] #Back surface
    face6 = [points[4], points[2], points[1], points[7]] #Right surfaceg

    polygons = [face1, face2, face3, face4, face5, face6]
    # polygons should hold all points (list or tuple) that make up the faces of the cube
    # each polygon will consist of points from the list 'points'
    # i.e., polygons = [(points[0], points[1], points[2], points[3]), ... other faces ...] 
    # make sure that the points are given in clockwise (or counter clockwise) order
    

    # sort by z-coordinate, big to small
    polygons = sorted(polygons, key=lambda polygon: -depth(polygon))

    # draw the polygons
    for poly in polygons:
        # assumes that each polygon has 4 sides
        p1 = poly[0]
        p2 = poly[1]
        p3 = poly[2]
        p4 = poly[3]
        
        polygon = Polygon(Point(projectX(p1[0], p1[2]), projectY(p1[1], p1[2])), Point(projectX(p2[0], p2[2]), projectY(p2[1], p2[2])), Point(projectX(p3[0], p3[2]), projectY(p3[1], p3[2])), Point(projectX(p4[0], p4[2]), projectY(p4[1], p4[2])))
        polygon.setFill(color_rgb(randint(0, 255), randint(0, 255), randint(0, 255))) # color in a random color
        polygon.draw(win)

        win.getMouse() # wait for a mouse click between polygons
        

    # close the graphics window
    win.close()

if __name__ == "__main__":
    main()
