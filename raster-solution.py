# rasterization homework
# # CS 314, Denison University

from graphics import *
from math import *
from random import *

# Constants #
pixHeight = 400    # height of screen in pixels
pixWidth = 400     # width of screen in pixels
d = 1.0            # distance of eye  from screen in world units
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


def cmp(a, b):
    ''' returns 1 if a>b, -1 if b>a, and 0 if equal '''
    return (a > b) - (a < b)

def drawPolygon(p, win, color):
    ''' draws polygon onto screen g using rasterization algorithm '''
    n = len(p)   # number of vertices in polygon
    x = []       # x-coordinates of polygon on screen
    y = []       # y-coordinates of polygon on screen
    for point in p:
        x.append(projectX(point[0], point[2]))
        y.append(projectY(point[1], point[2]))

    # get the upper and lower limits of the scanlines
    minY = int(min(y))
    maxY = int(max(y))
    
    # find bounds on scan lines
    minX = [infinity for i in range(maxY - minY + 1)]
    maxX = [-infinity for i in range(maxY - minY + 1)]  
    for i in range(n):
        x1 = int(x[i])
        y1 = int(y[i])
        x2 = int(x[(i + 1) % n])
        y2 = int(y[(i + 1) % n])
        if x2 != x1:
            m = float(y2 - y1)/(x2 - x1)
            for xLine in range(x1, x2, cmp(x2, x1)):
                yLine = int(y1 + m * (xLine - x1)) 
                minX[yLine - minY] = min(minX[yLine - minY], xLine)
                maxX[yLine - minY] = max(maxX[yLine - minY], xLine)
        else:
            for yLine in range(min(y1, y2), max(y1, y2)):
                minX[yLine - minY] = min(minX[yLine - minY], x1)
                maxX[yLine - minY] = max(maxX[yLine - minY], x1)
                
    # now draw the scan lines
    resolution = 3
    for yDraw in range(minY, maxY, resolution):
        for xDraw in range(minX[yDraw - minY], maxX[yDraw - minY], resolution):
            drawPoint(xDraw, yDraw, resolution, color, win)

    # draws in the bounding polygon
    for i in range(n):
        x1 = int(x[i])
        y1 = int(y[i])
        x2 = int(x[(i + 1) % n])
        y2 = int(y[(i + 1) % n])
        line = Line(Point(x1, y1), Point(x2, y2))
        line.draw(win)

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
        color = color_rgb(randint(0, 255), randint(0, 255), randint(0, 255))
        drawPolygon(p, win, color)
        win.getMouse()

  
    win.getMouse()
    win.close()


if __name__ == "__main__":
	main()
