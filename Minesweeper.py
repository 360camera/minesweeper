from random import randint
from rich import print
import os

"""
TODO:
Add flagging spaces as mines
Add win condition
Add menu with board selection
Add leaderboard with times
"""

class Minesweeper:
    # Generates a minesweeper board
    # Use self.board to see the complete board
    # Use self.obscuredBoard to see a solvable board

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
        self.gameState = True

    def revealSpace(self, spaceX, spaceY): # Reveal space (spaceX,spaceY) on obscuredBoard
        if self.board[spaceY][spaceX] != 0:
            self.obscuredBoard[spaceY][spaceX] = self.board[spaceY][spaceX]
            if self.board[spaceY][spaceX] == "X":
                self.gameState = False # You died
        else:
            self.revealEmpties(spaceX, spaceY)
    
    def printColor(self, obscure=True): # Print board with color, specify False for completed board
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
m = Minesweeper(10,10,10)
while True:
    os.system("cls")
    m.printColor()
    if m.gameState == False:
        print("[red]GAME OVER![/red]")
        exit()
    x = int(input("X: "))
    y = int(input("Y: "))
    m.revealSpace(x-1, y-1)
