# rasterization homework
# CS 314, Denison University

from graphics import *
from math import *
from random import *
import sys

# Constants #
pixHeight = 400    # height of screen in pixels
pixWidth = 400     # width of screen in pixels
d = 1.0            # distance of eye from screen in world units
screenWidth = 1.0  # width of screen in world size
screenHeight = 1.0 # height of screen in world size 
infinity = 100000  # needed for max and min

def projectX(x, z):
    ''' maps x to screen x location '''
    return pixWidth / 2 + (pixWidth / screenWidth) * x * d / (z + d)

def projectY(y, z):
    ''' maps y to screen y location '''
    return pixHeight / 2 + (pixHeight / screenHeight) * y * d / (z + d)

def forward(point, distance):
    ''' update point when player moves forward given distance '''
    point[2] -= distance

def backward(point, distance):
    ''' update point when player moves backward given distance '''
    point[2] += distance

def rotate(point, angle, center):
    ''' rotates the polygon 'angle' radians around the point 'center'
    point: a 3D point represented by a list of size 3
    angle: an angle in radians
    center: the point around which we are rotating the point
    '''
    
    # center point on rotation center
    for i in range(3):
        point[i] = point[i] - center[i]

    # use the rotation formula
    x = point[0] * cos(angle) + point[2] * sin(angle)
    z = point[2] * cos(angle) - point[0] * sin(angle)
    point[0] = x
    point[2] = z
        
    # un-center point on rotation center
    for i in range(3):
        point[i] = point[i] + center[i]

def depth(polygon):
    ''' the average depth of a polygon, represented as a list of points '''
    return sum([point[2] for point in polygon])/len(polygon) # average of z-coordinate

def drawPoint(x, y, size, color, win):
    ''' draws a size X size rectangle on win at given coordinates
    with given color
    '''
    pt = Rectangle(Point(x, y), Point(x + size, y + size))
    pt.setFill(color)
    pt.setOutline(color)
    pt.draw(win)


def drawPolygon(p, win, color):
    ''' draws polygon onto screen g using rasterization algorithm '''
    n = len(p)   # number of vertices in polygon
    x = []       # x-coordinates of polygon on screen
    y = []       # y-coordinates of polygon on screen
    for point in p:
        x.append(projectX(point[0], point[2]))
        y.append(projectY(point[1], point[2]))

    pc = []
    for i in range(n):
        newco = []
        newco.append(x[i])
        newco.append(y[i])
        pc.append(newco) # Creating a new list with the (x,y) points in terms of the actual screen size


    # get the upper and lower limits of the scanlines
    y_min = min(y)
    y_max = max(y)

    x_min = []
    x_max = []
        
    # find bounds on scan lines
    for i in range(0, int(y_max+1-y_min)):
        x_min.append(9223372036854775807) #storing positive infinity for all x_min
        x_max.append(-9223372036854775806) #stroring negative infinity for all x_max
        

    # now draw the scan lines
    resolution = 3

    # YOUR CODE GOES HERE
    for i in range(n): # For each point in pc
        if(i != n-1): # Except the last point
                p1 = pc[i] # We take the current and the next point to get the coordinates of one of the lines of the polygons
                p2 = pc[i+1] 
        else: # In the case that this is the last point of the polygon, it will be connected to the first point again 
                p1 = pc[i]
                p2 = pc[0]
                        
        if(p1[0] > p2[0]): # If the x-coordinate of the first point is bigger than that of the second point, we switch the points and then draw the lines
            temp = p2
            p2 = p1;
            p1 = temp
            
        if(p1[0] != p2[0]): # In the case that the line is not a vertical line
            sl = (p2[1] - p1[1])/(p2[0] - p1[0]) # We find the slope
            for i in range(int(p1[1] - y_min), int(p2[1] - y_min)): # For each y value between point 1 and point 2, we find the x value
                    xval = (int)((i + y_min) - p1[1])/sl # we use the formula y = mx + c for this purpose
                    x_min[i] = min(xval, x_min[i]) # Updating the x_min value for y
                    x_max[i] = max(xval, x_max[i]) # Updating the x_max value for y
        else:
            for i in range(int(p1[1] - y_min), int(p2[1]+1 - y_min)): # In the case that the line is a vertical line
                x_min[i] = min(p1[0], x_min[i]) # Adjust x_min according to the value of point x
                x_max[i] = max(p1[0], x_max[i]) # Adjus x_max according to the value of point x
            

    # The following draws a point at (x, y) of color 'color'
    # size controls the size of the point (to speed up drawing)
    # drawPoint(x, y, size, color, win)
    # for example:
    # drawPoint(100, 100, 1, color, win)
    

    # draws in the bounding polygon
    for i in range(n):
        x1 = int(x[i])
        y1 = int(y[i])
        x2 = int(x[(i + 1) % n])
        y2 = int(y[(i + 1) % n])
        line = Line(Point(x1, y1), Point(x2, y2))
        line.draw(win)
                        
    for i in range(0, int(y_max - y_min)): # Going through each y line
        for j in range(int(x_min[i]), int(x_max[i])): # Going through x_min to x_max to print the scan lines for each y coordinate
            drawPoint(j, (i + y_min), 1, color, win) 

def main():
    ''' Main program that runs everything '''
   
    win = GraphWin("Projection", pixHeight, pixWidth)

    # create points on a cube
    points = []
    for x in range(-1, 2, 2):
        for y in range(-1, 2, 2):
            for z in range(5, 8, 2):
                points.append([x, y, z])

    # rotate around center by 45 degrees
    for p in points:
        rotate(p, 3.14/4, [0, 0, 6])

    # create the polygons for the 6 faces of a cube
    polygons = [[points[0], points[2], points[6], points[4]],  # front
                [points[1], points[3], points[7], points[5]],  # back
                [points[2], points[3], points[7], points[6]],  # top
                [points[0], points[1], points[5], points[4]],  # bottom
                [points[0], points[1], points[3], points[2]],  # left
                [points[4], points[5], points[7], points[6]]]  # right

    # sort points by z-axis (draw farther points first)
    polygons = sorted(polygons, key=lambda polygon: -depth(polygon))

    # draw all the polygons
    for p in polygons:
        print(p)
        color = color_rgb(randint(0, 255), randint(0, 255), randint(0, 255))
        drawPolygon(p, win, color)
        win.getMouse()

  
    win.getMouse()
    win.close()


if __name__ == "__main__":
    main()
