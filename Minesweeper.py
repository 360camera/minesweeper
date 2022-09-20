from random import randint
from rich import print
import os

class Minesweeper:
    # Generates a minesweeper board
    # Use self.board to see the complete board
    # Use self.obscuredBoard to see a solvable board

    # Internal functions

    def placeMine(self, board, placeX, placeY): # Place a mine on the board
        board[placeY][placeX] = "X"
        # Increment tiles around mine
        for modY in range(-1,2):
            for modX in range(-1,2):
                if placeY+modY in range(0,len(board)) and placeX+modX in range(0,len(board[0])):
                    if board[placeY+modY][placeX+modX] != "X":
                        board[placeY+modY][placeX+modX] += 1
        return board

    def printBlack(self): # prints top black line
        x = len(self.board[0])+2
        line = "[black]"
        for i in range(x):
            if i == 0:
                line += "O-"
            elif i == x-1:
                line += "O"
            else:
                line += "--"
        print(line + "[/black]")
        
    def revealEmpties(self, spaceX, spaceY): # Reveal empty tiles around a space
        for coords in [(0,0), (1,0), (-1,0), (0,1), (0,-1), (1,1), (-1,1), (1,-1), (-1,-1)]: # TODO: this wasn't always this weird - fix it
            checkX, checkY = spaceX+coords[0], spaceY+coords[1]
            if checkY in range(len(self.board)) and checkX in range(len(self.board[0])):
                actualTile = self.board[checkY][checkX]
                # Tile not already revealed
                if self.obscuredBoard[checkY][checkX] == "?":
                    # Tile is a zero, reveal all around it
                    if actualTile == 0:
                        self.obscuredBoard[checkY][checkX] = 0
                        self.revealEmpties(checkX, checkY)
                    # Tile is on the edge and isn't a mine, reveal only it
                    elif coords != (0,0) and actualTile != "X":
                        self.obscuredBoard[checkY][checkX] = actualTile

    # revealEmpties OLD VERSION (kept in case i mega screwed up)

    """def revealEmpties(self, spaceX, spaceY): # Reveal empty tiles around a space
        for coords in [(0,0), (1,0), (-1,0), (0,1), (0,-1)]: # in plus shape around tile
            if spaceY+coords[1] in range(len(self.board)) and spaceX+coords[0] in range(len(self.board[0])):
                if self.obscuredBoard[spaceY+coords[1]][spaceX+coords[0]] != "?":
                    print("Already cleared")
                elif self.board[spaceY+coords[1]][spaceX+coords[0]] == 0:
                    checkX = spaceX+coords[0]
                    checkY = spaceY+coords[1]
                    # Count surrounding mines
                    mines = 0
                    for modX in range(-1, 2):
                        for modY in range(-1, 2):
                            if modX+checkX in range(len(self.board[0])) and modY+checkY in range(len(self.board)):
                                if self.board[checkY+modY][checkX+modX] == "X" and (modX, modY) != (0,0):
                                    mines += 1
                    # Reveal
                    self.obscuredBoard[checkY][checkX] = mines
                    # Repeat if nessecary
                    #if not isFirst and mines != 0:
                        #return
                    if mines == 0: # this may be redundant, need to test
                        self.revealEmpties(checkX, checkY)
                    else:
                        print("No mines")
                        exit()
                elif coords != (0,0) and self.board[spaceY+coords[1]][spaceX+coords[0]] != "X":
                    self.obscuredBoard[spaceY+coords[1]][spaceX+coords[0]] = self.board[spaceY+coords[1]][spaceX+coords[0]]
                    print("copied")"""

    def __init__(self, width, height, mines): # Create a widthXheight board with mines
        # Generate boards
        board = []
        obscuredBoard = []
        for y in range(height):
            board.append([])
            obscuredBoard.append([])
            for x in range(width):
                board[-1].append(0)
                obscuredBoard[-1].append("?")
        # Place mines
        minesPlaced = 0
        while minesPlaced < mines:
            placeX, placeY = randint(0,width-1), randint(0,height-1)
            if board[placeY][placeX] != "X":
                board = self.placeMine(board, placeX, placeY)
                minesPlaced += 1
        self.board = board
        self.obscuredBoard = obscuredBoard

    def revealSpace(self, spaceX, spaceY): # Reveal space (spaceX,spaceY) on obscuredBoard
        if self.board[spaceY][spaceX] != 0:
            self.obscuredBoard[spaceY][spaceX] = self.board[spaceY][spaceX]
        else:
            self.revealEmpties(spaceX, spaceY)
    
    def printColor(self, obscure): # Print board with color!
        if obscure:
            usingBoard = self.obscuredBoard
        else:
            usingBoard = self.board
        # Print
        self.printBlack()
        for x in usingBoard:
            line = "[black]| [/black]"
            for y in x:
                if y == "?":
                    color = "grey93"
                elif y == "X":
                    color = "red"
                else:
                    color = ["dark_green", "tan", "yellow3", "orange1", "dark_orange", "orange_red1", "red1", "dark_red", "magenta"][y]
                line += "[" + color + "]" + str(y) + "[/" + color + "] "
            line += "[black]|[/black]"
            print(line)
        self.printBlack()



# execution
t = Minesweeper(10,10,10)
while True:
    os.system("cls")
    t.printColor(True)
    x = int(input("X: "))
    y = int(input("Y: "))
    t.revealSpace(x-1, y-1)

"""for x in t.board:
    line = ""
    for y in x:
        line += str(y) + " "
    print(line)"""
