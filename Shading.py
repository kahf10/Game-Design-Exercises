# shading homework
# CS 314, Denison University

import math
from graphics import *
from math import *
from random import *
from time import *

# Constants #
pixHeight = 400    # height of screen in pixels
pixWidth = 400     # width of screen in pixels
d = 1.0            # distance of eye from screen in world units
screenWidth = 1.0  # width of screen in world size
screenHeight = 1.0 # height of screen in world size 
infinity = 100000  # needed for max and min
PI = 3.1415926535897932384626433 # number of decimal places Dr. Lall has memorized

def projectX(x, z):
    ''' maps x to screen x location '''
    return pixWidth / 2 + (pixWidth / screenWidth) * x * d / (z + d)

def projectY(y, z):
    ''' maps y to screen y location '''
    return pixHeight / 2 + (pixHeight / screenHeight) * y * d / (z + d)

def drawPoint(x, y, size, color, g):
    ''' draws a size X size rectangle on g at given coordinates
    with given color '''
    pt = Rectangle(Point(x, y), Point(x + size, y + size))
    pt.setFill(color)
    pt.setOutline(color)
    pt.draw(g)

def rotate(p, angle, center):
    ''' rotates the 3D point 'angle' radians around the point 'center'
    pre-condition: The point p should be a LIST with 3 elements '''

    # center point on rotation center
    for i in range(3):
        p[i] = p[i] - center[i]
    
    x = p[0] * cos(angle) - p[2] * sin(angle)
    z = p[2] * cos(angle) + p[0] * sin(angle)
    p[0] = x
    p[2] = z
        
    # un-center point on rotation center
    for i in range(3):
        p[i] = p[i] + center[i]


def mag(v):
    ''' returns the magnitude of a vector v '''
    # FILL YOUR CODE IN HERE
    
    x = v[0]
    y = v[1]
    z = v[2]

    magnitude = math.sqrt((x*x) + (y*y) + (z*z))
    return magnitude

    
def cross(u, v):
    ''' computes cross product of two vectors
    pre-condition: each vector is a list with 3 elements '''
    # FILL YOUR CODE IN HERE
    
    x1 = u[0]
    y1 = u[1]
    z1 = u[2]

    x2 = v[0]
    y2 = v[1]
    z2 = v[2]

    cp = []
    cp.append((y1*z2) - (z1*y2))
    cp.append((z1*x2) - (x1*z2))
    cp.append((x1*y2) - (y1*x2))

    return cp
    
def dot(u, v):
    ''' computes cross product of two vectors
    pre-condition: each vector is a list with 3 elements '''
    # FILL YOUR CODE IN HERE
    
    x1 = u[0]
    y1 = u[1]
    z1 = u[2]

    x2 = v[0]
    y2 = v[1]
    z2 = v[2]

    dp = x1*x2 + y1*y2 + z1*z2
    
    return dp 

def drawPolygon(p, w):   
    ''' draws shaded polygon '''

    # direction of light source 
    light = [1, 0, 1]
    #light = [1, 0, 0]  # from the left

    # make the light vector into a unit vector
    lightmag = mag(light)
    for i in range(3):
        light[i] /= lightmag

    ### Compute the shade of the polygon ###
    ##############################################################
    # FILL YOUR CODE IN HERE
    
    # compute two edge vectors of polygon

    e1 = [p[2][0] - p[0][0], p[2][1] - p[0][1], p[2][2] - p[0][2]]
    e2 = [p[3][0] - p[0][0], p[3][1] - p[0][1], p[3][2] - p[0][2]]

    # use cross product to get normal vector (and make into a unit vector)
    
    nv = cross(e1, e2)
  
    unv = []
    unv.append(nv[0] / mag(nv)*1)
    unv.append(nv[1] / mag(nv)*1)
    unv.append(nv[2] / mag(nv)*1)
    
    # use dot product to compute cosine of angle between normal and light
    
    cosine = dot(unv, light)

    ##############################################################

    # estimate shade of polygon based on cos of angle
    shade = 128 + int(96 * cosine)
    color = color_rgb(shade, shade, shade)

    ## Project and draw in the polygon ##
    polygon = []
    for point in p:
        polygon.append(Point(projectX(point[0], point[2]), projectY(point[1], point[2])))
    poly = Polygon(polygon)
    poly.setFill(color)
    poly.setOutline(color)
    poly.draw(w)
    
    w.update()
            
# computes the average z value of a face
def avgZ(polygon):
    return float(sum([point[2] for point in polygon]))/len(polygon)

def main():
    ''' Main program '''

    g = GraphWin("Shading", pixHeight, pixWidth, autoflush=False)

    # get points on a sphere
    res = 30
    radius = 1
    points = [[None for i in range(res)] for j in range(res)]
    for theta in range(res):
        for phi in range(res):
            x = radius * cos(2 * PI * theta / res) * sin(PI * phi / res)
            y = radius * sin(2 * PI * theta / res) * sin(PI * phi / res)
            z = 3 + radius * cos(PI * phi / res)
            points[theta][phi] = [x, y, z]

            # rotate around center by 90 degrees
            rotate(points[theta][phi], 3.14/2, [0, 0, 3])
         
    # create the polygons for a sphere
    polygons = []
    for i in range(res-1):
        for j in range(res-1):
            polygons.append([points[i][j], points[i+1][j], points[i+1][j+1], points[i][j+1]])
        

    # sort points by z-axis (draw farther points first)
    polygons = sorted(polygons, key=avgZ, reverse=True)


    # draw all the polygons
    for p in polygons:
        drawPolygon(p, g)
        #g.getMouse()
      
    g.getMouse()
    g.close()

if __name__ == "__main__":
    main()
