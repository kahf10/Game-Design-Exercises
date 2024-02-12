# Minimax homework
# CS 314, Denison University

from graphics import *

# parameters of the game
n = 5     # width
m = 5     # height
k = 4     # how many in a row needed for a win

depth = 3 # depth of AI search

# function to check if either player has won
# returns 0 if no player has won
# returns 1 if player one has won
# returns 2 if player two has won
def winner(b):
    # check horizontal
    for i in range(0, n - k + 1):
        for j in range(m):            
            if b[i][j] != 0:
                allSame = True
                for l in range(k):
                    if b[i + l][j] != b[i][j]:
                        allSame = False
                if allSame:
                    return b[i][j]
            
    # check vertical
    for i in range(n):
        for j in range(m - k + 1):            
            if b[i][j] != 0:
                allSame = True
                for l in range(k):
                    if b[i][j + l] != b[i][j]:
                        allSame = False
                if allSame:
                    return b[i][j]
            
    # check NW-SE diagonal
    for i in range(n - k + 1):
        for j in range(m - k + 1):            
            if b[i][j] != 0:
                allSame = True
                for l in range(k):
                    if b[i + l][j + l] != b[i][j]:
                        allSame = False
                if allSame:
                    return b[i][j]
    
    # check NE-SW diagonal
    for i in range(n - k + 1):
        for j in range(k - 1, m):            
            if b[i][j] != 0:
                allSame = True
                for l in range(k):
                    if b[i + l][j - l] != b[i][j]:
                        allSame = False
                if allSame:
                    return b[i][j]
            
    return 0

# minimax algorithm

def minimax(b, p, d):
    ''' returns the minimax rating of the board b
        for player p (1 or 2) using depth d '''

    if(d <= 0):
        return
    a = float('-inf')
    for x1 in range(n):
        for y1 in range(m):
            a = max(a, -minimax(b, p, d-1)
    
    
def move(b, p, d):
    ''' returns the best move (as a tuple of column, row)
        for player p (1 or 2) using minimax with depth d '''

    best = float('-inf') #Best = - infinity
    bestMove = (0, 0) # bestMove = None
    for x in range(n):
        for y in range(m): #For each Child
            if (b[x][y] == 0): #If there is no move played on that location
                b[x][y] = p #Gives a temporary marker to that location
                if(p == 1): #If player 1 is playing, it calculates the damage suffered by player 2
                    m = -minimax(b, 2, d-1)
                elif(p == 2):
                    m = -minimax(b, 1, d-1) #And if player 2 is playing, it calculates the damage suffered by player 1
                if m > best: #if m > best
                    best = m #best = m
                    bestMove = b[x][y] #bestMove = current child
                b[x][y] = 0 #Restting the given location for the next iteration
    
    return bestMove


def main():
    # graphics parameters
    height = 500
    width = 500

    g = GraphWin("n,m,k-game", width, height)

    # draw the board
    for i in range(1, n):
        l = Line(Point(i * width/n, 0), Point(i * width/n, height))
        l.draw(g)
    for i in range(1, m):
        l = Line(Point(0, i * height/m), Point(width, i  * height/m))
        l.draw(g)

    # the board is represented by a 2D list (matrix) in which
    # empty squares have a 0 in them 
    # player 1 squares have a 1 in them
    # player 2 squares have a 2 in them
    board = [[0 for i in range(n)] for j in range(m)]

    moves = 0  # counts number of moves
    turn = 1
    while winner(board) == 0 and moves < n * m:
        if turn == 1:
            # player picks a move
            x = y = -1
            while x == -1 or board[x][y] != 0:
                p = g.getMouse()
                x = int(p.getX()/(width/n))
                y = int(p.getY()/(height/m))
        else:
            # computer picks a move looking ahead 3 moves
            (x, y) = move(board, 2, depth)
                
        # make the move
        board[x][y] = turn
        t = Text(Point((x + .5) * width/n, (y + .5) * height/m), str(turn))
        t.setSize(30)
        t.draw(g)
        
        turn = 3 - turn # alternates 1 & 2    
        moves += 1

    # display the result of the game
    victor = winner(board)
    if victor == 0:
        text = "Draw"
    elif victor == 1:
        text = "You win"
    else:
        text = "You lose"
    t = Text(Point(width/2, height/2), text)
    t.setSize(35)
    t.setFill("red")
    t.draw(g)



    g.getMouse()
    g.close()

if __name__ == "__main__":
    main()
