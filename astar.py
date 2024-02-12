# A* search homework
# CS 314, Denison University

from graphics import *
from time import *

# width and height of graphics screen
WIDTH = 800
HEIGHT = 600
INFINITY = 1000000000  
   
# read in the map into a matrix, m (0 is empty cell, 1 is an impassable cell)
# source into a list, src
# destination into a list, dst
def loadMap(mapName):
    f = open(mapName, "r")
    meta = f.readline()
    rowcol = meta.split()
    rows = int(rowcol[0])
    cols = int(rowcol[1])
    m = [[0 for i in range(cols)] for j in range(rows)]
    src = [0, 0]  # coordinate of starting point
    dst = [0, 0]  # coordinate of ending point 
    for i in range(rows):
        line = f.readline()
        for j in range(cols):
            if line[j] == "#":
                m[i][j] = 1   # Wall at this location
            elif line[j] == "1":
                src = [i, j]
            elif line[j] == "2":
                dst = [i, j]
    return m, src, dst

# fills in cell (i, j) in graphics window
def fillCell(w, i, j, m, color):
    rows = len(m)
    cols = len(m[0])
    r = Rectangle(Point(i * WIDTH/cols, j * HEIGHT/rows), Point((i + 1) * WIDTH/cols, (j + 1) * HEIGHT/rows))
    r.setFill(color)
    r.draw(w)

# draw the map
def drawMap(m, src, dst):
    w = GraphWin("A* example", WIDTH, HEIGHT)
    rows = len(m)
    cols = len(m[0])
    for i in range(rows):
        for j in range(cols):
            if m[i][j] == 1:
                fillCell(w, i, j, m, "black")

    # draw source and destination
    fillCell(w, src[0], src[1], m, "green")
    fillCell(w, dst[0], dst[1], m, "red")
    
    return w



def Dijkstra(w, m, src, dst):
    rows = len(m)
    cols = len(m[0])

    # get mappings from coordinate in grid to node and vice versa
    node = 0
    nodeToCoord = {}
    coordToNode = {}
    for i in range(rows):
        for j in range(cols):
            nodeToCoord[node] = (i, j)
            coordToNode[(i, j)] = node
            node = node + 1

    # populate adjacency matrix
    dist = [[INFINITY for i in range(rows * cols)] for j in range(rows * cols)]
    for i in range(rows):
        for j in range(cols):
            if m[i][j] == 0:
                if i > 0 and j > 0 and m[i-1][j-1] == 0:
                    dist[coordToNode[(i, j)]][coordToNode[(i - 1, j - 1)]] = 14 # NW
                if i > 0 and m[i-1][j] == 0:
                    dist[coordToNode[(i, j)]][coordToNode[(i - 1, j)]] = 10     # N
                if i > 0 and j < cols - 1 and m[i-1][j+1] == 0:
                    dist[coordToNode[(i, j)]][coordToNode[(i - 1, j + 1)]] = 14 # NE 
                if j > 0 and m[i][j-1] == 0:
                    dist[coordToNode[(i, j)]][coordToNode[(i, j - 1)]] = 10     # W
                if j < cols - 1 and m[i][j+1] == 0:
                    dist[coordToNode[(i, j)]][coordToNode[(i, j + 1)]] = 10     # E
                if i < rows - 1 and j > 0 and m[i+1][j-1] == 0:
                    dist[coordToNode[(i, j)]][coordToNode[(i + 1, j - 1)]] = 14 # SW
                if i < rows - 1 and m[i+1][j] == 0:
                    dist[coordToNode[(i, j)]][coordToNode[(i + 1, j)]] = 10     # S
                if i < rows - 1 and j < cols - 1and m[i+1][j+1] == 0:
                    dist[coordToNode[(i, j)]][coordToNode[(i + 1, j + 1)]] = 14 # SE

    # now perform Dijkstra's algorithm search on graph
    d = {}
    previous = {}
    for i in range(rows * cols):
        d[i] = INFINITY
        previous[i] = None
    u = coordToNode[(src[0], src[1])] # start with source
    destination = coordToNode[(dst[0], dst[1])]
    d[u] = 0
    Q = [i for i in range(rows * cols)]
    while u != destination:
        # find unvisited node with smallest distance
        u = Q[0]
        for i in range(1, len(Q)):
            if d[Q[i]] < d[u]:
                u = Q[i]
        Q.remove(u)

        (i, j) = nodeToCoord[u]
        fillCell(w, i, j, m, "yellow")
        sleep(0.05)

        if d[u] == INFINITY:
            # No path available
            return

        for v in range(rows * cols):
            if dist[u][v] < INFINITY: # neighbors
                alt = d[u] + dist[u][v]
                if alt < d[v]:
                    d[v] = alt
                    previous[v] = u

    S = []            
    while previous[u] != None:
        S = [u] + S  # prepend u to S
        u = previous[u]

    for v in S:
        (i, j) = nodeToCoord[v]
        fillCell(w, i, j, m, "blue")
                                    
def Astar(w, m, src, dst):
    node = 0
    nodeToCoord = {}
    coordToNode = {}
    for i in range(rows):
        for j in range(cols):
            nodeToCoord[node] = (i, j)
            coordToNode[(i, j)] = node
            node = node + 1

    # populate adjacency matrix
    dist = [[INFINITY for i in range(rows * cols)] for j in range(rows * cols)]
    for i in range(rows):
        for j in range(cols):
            if m[i][j] == 0:
                if i > 0 and j > 0 and m[i-1][j-1] == 0:
                    dist[coordToNode[(i, j)]][coordToNode[(i - 1, j - 1)]] = 14 # NW
                if i > 0 and m[i-1][j] == 0:
                    dist[coordToNode[(i, j)]][coordToNode[(i - 1, j)]] = 10     # N
                if i > 0 and j < cols - 1 and m[i-1][j+1] == 0:
                    dist[coordToNode[(i, j)]][coordToNode[(i - 1, j + 1)]] = 14 # NE 
                if j > 0 and m[i][j-1] == 0:
                    dist[coordToNode[(i, j)]][coordToNode[(i, j - 1)]] = 10     # W
                if j < cols - 1 and m[i][j+1] == 0:
                    dist[coordToNode[(i, j)]][coordToNode[(i, j + 1)]] = 10     # E
                if i < rows - 1 and j > 0 and m[i+1][j-1] == 0:
                    dist[coordToNode[(i, j)]][coordToNode[(i + 1, j - 1)]] = 14 # SW
                if i < rows - 1 and m[i+1][j] == 0:
                    dist[coordToNode[(i, j)]][coordToNode[(i + 1, j)]] = 10     # S
                if i < rows - 1 and j < cols - 1and m[i+1][j+1] == 0:
                    dist[coordToNode[(i, j)]][coordToNode[(i + 1, j + 1)]] = 14 # SE

    d = {}
    previous = {}
    h = {}
    g = {}
    f = {}
    cset = {} #Initialize Closed Set
    oset = {} #Initialize Open Set
    pred = {}

    destination = coordToNode[(dst[0], dst[1])] #Finding Destination
    for i in range(rows * cols):
        d[i] = INFINITY
        previous[i] = None
    
    for i in range(rows):
        for j in range(cols):
            h[coordToNode[(i,j)]] = math.sqrt((i - dst[0])**2 + (j - dst[1])**2)  #Finding h[v] for all nodes
    
    oset.add(src) #Initializing open set with source
    g[src] = 0 # Initializing g with source
    f(src) = h[src] + g[src] # Initializing the value for f[src]

    while len(oset) != 0: #While open set is not empty
        u = oset[0]
        for i in oset: #Finding the node in open set with the smallest f value
            if f[u] > f[i]:
                u = i
        oset.remove(u) # Removing u from open set
        cset.add(u) # Adding u to closed set 
        if(u == dst): #Checking if we reached destination or not
            break;
        for v in range(rows * cols): #Going through the neighbors
            if dist[u][v] < INFINITY: # neighbors
                if v not in cset: # If v is not in closed set
                    if v not in oset: # If v is not in open set
                        oset.add(v) #Add v to open set
                        pred[v] = u #Make u the predecessor of v
                        g[v] = g[u] + dist[u][v] # Finding the g value for v
                        f[v] = g[v] + h[v] # Finding the f value for v
                    elif g[u] + dist[u][v] <= g[v]:
                        pred[v] = u #Making u the predecessor of v
                        g[v] = g[u] + dist[u][v] 
                        f[v] = g[v] + h[v]
            (i, j) = nodeToCoord[u]
            fillCell(w, i, j, m, "yellow") # Filling nodes yellow as we explore them

    if dst not in cset: # In the case that the dst is not found
        print("Search Failed")
    else:
        for v in cset: # If destination is found, we color the shortest path blue
        (i, j) = nodeToCoord[v]
        fillCell(w, i, j, m, "blue")


def main():
    for level in ["maps/toronto.txt", "maps/vee.txt", "maps/gate.txt", "maps/oval.txt", "maps/quadrant.txt", "maps/trix.txt", "maps/u.txt"]:
        m, src, dst = loadMap(level)

        # run Dijkstra
        w = drawMap(m, src, dst)
        Dijkstra(w, m, src, dst)
        w.getMouse()
        w.close()

        # run A*
        w = drawMap(m, src, dst)
        Astar(w, m, src, dst)
        w.getMouse()
        w.close()


if __name__ == "__main__":
    main()
