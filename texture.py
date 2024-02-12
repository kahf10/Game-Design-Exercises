# texture-mapping homework
# CS 314, Denison University

from graphics import *
from math import *
from random import *

# Constants #
pixHeight = 400    # height of screen in pixels
pixWidth = 400     # width of screen in pixels
d = 1.0            # distance of eye from screen in world units
screenWidth = 1.0  # width of screen in world size
screenHeight = 1.0 # height of screen in world size 
infinity = 100000  # needed for max and min

# maps x to screen x location
def projectX(x, z):
    return pixWidth / 2 + (pixWidth / screenWidth) * x * d / (z + d)

# maps y to screen y location
def projectY(y, z):
    return pixHeight / 2 + (pixHeight / screenHeight) * y * d / (z + d)

# rotates the 3D point 'angle' radians around the point 'center'
# pre-condition: The point p should be a LIST with 3 elements
def rotate(p, angle, center):
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

# draws a texel in window w at given position, size, and color
def drawTexel(w, x, y, color):       
    texel = Point(x, y)
    texel.setFill(color)
    texel.draw(w)
    
# draws polygon my mapping each pixel using a bilinear mapping
def drawPolygon(poly, w, texture):
    textureHeight = len(texture[0])
    textureWidth = len(texture)

    # BILINEAR TEXTURE-MAPPING CODE GOES HERE
    # Note 1: drawTexel(w, x, y, c) draws a texel at screen position (x, y) of color c
    # Note 2: texture[x][y] refers to the the texture color at (x, y) in the texture 

    for i in range(textureWidth):
        for j in range(textureHeight):
            alpha = i / textureWidth
            beta = j / textureHeight

            xpos = ((1-alpha) * (1-beta) * poly[0][0]) + (alpha * (1 - beta) * poly[1][0]) + ((1-alpha) * beta * poly[3][0]) + (alpha * beta * poly[2][0])
            ypos = ((1-alpha) * (1-beta) * poly[0][1]) + (alpha * (1 - beta) * poly[1][1]) + ((1-alpha) * beta * poly[3][1]) + (alpha * beta * poly[2][1])
            zpos = ((1-alpha) * (1-beta) * poly[0][2]) + (alpha * (1 - beta) * poly[1][2]) + ((1-alpha) * beta * poly[3][2]) + (alpha * beta * poly[2][2])

            drawTexel(w, projectX(xpos, zpos), projectY(ypos, zpos), texture[i][j])
    
    w.update()
            
# computes the average z value of a face
def avgZ(polygon):
    return float(sum([point[2] for point in polygon]))/len(polygon)

# Main program #
def main():
    g = GraphWin("Texture", pixHeight, pixWidth, autoflush=False)

    # load, draw, and capture companion cube texture
    img = Image(Point(200, 200), "companion.gif")
    texture = [[color_rgb(img.getPixel(j, i)[0], img.getPixel(j, i)[1], img.getPixel(j, i)[2]) for i in range(img.getHeight())] for j in range(img.getWidth())]
        
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
    polygons = sorted(polygons, key=avgZ, reverse=True)


    # draw all the polygons
    for p in polygons:
        drawPolygon(p, g, texture)
        g.getMouse()

      
    g.getMouse()
    g.close()


if __name__ == "__main__":
    main()
