#! /usr/bin/python3
# author: Todd Gaunt
# apache 2.0
# minesweeper game

import random, os, curses

#TODO implement object oriented minesweeper

def main():
    # initializing parameters of the game, such as win/lose conditions, difficulty, and generating the board.
    victory = False
    explosion = False
    boardSize = 10
    difficulty = "normal" # placeHolder for now
    board = boardGen(boardSize, 0) # Array holds the actual data
    cover = boardGen(boardSize, "#") # The array the player sees and slowly "uncovers" to see the board beneath
    plantMines(board, difficulty)
    numberGen(board) #

    # The player starts playing here.
    while explosion == False and victory == False:
        os.system('clear') # refresh the screen.
        printBoard(cover)
        #printBoard(board) #for debugging, prints an uncovered board-state
        explosion = chooseTile(board, cover)
        victory = winCheck(cover, difficulty)

    # prints final boardState
    os.system('clear')
    printBoard(board)
    if victory == True:
        print("You Win!")
    else:
        print("You lose.")

# ARRAY FUNCTIONS
def boardGen(boardSize, tile):
    temp = []
    for y in range(boardSize):
        temp.append([])
        for x in range(boardSize):
            temp[y].append(tile)
    return temp

def printBoardSimple(board):
    boardSize = len(board)
    for y in range(boardSize):
        for x in range(boardSize):
            print (str(board[y][x])+" ", end="")
        print("")

def printBoard(board): # Adds a coordinates system for the user.
    boardSize = len(board)
    count = boardSize - 1
    for y in range(boardSize):
        print (str(count) + " - " , end="")
        for x in range(boardSize):
            print (str(board[y][x])+" ", end="")
        count -= 1
        print("")
    count = 0
    print("    ", end="")
    print("| " * boardSize)
    print("    ", end="")
    for i in range(boardSize):
        print(str(count) + " ", end="")
        count += 1
    print("")

# GAME LOGIC/INITIALIZATION
def plantMines(board, difficulty):
    boardSize = len(board)
    count = boardSize*1
    while count != 0:
        ypos = random.randint(0, boardSize - 1)
        xpos = random.randint(0, boardSize - 1)
        if board[ypos][xpos] == "X":
            count += 1
        else:
            board[ypos][xpos] = "X"
        count -= 1

def numberGen(board): # Generates the number tiles of the board, the number represents how many mines are adjacent to the tile.
    boardSize = len(board)
    for y in range(boardSize):
        for x in range(boardSize):
            if board[y][x] != "X":
                board[y][x] = 0
                # checks for mines laterally
                if x != len(board)-1 and board[y][x+1] == "X": #right
                    board[y][x] += 1
                if x != 0 and board[y][x-1] == "X": #left
                    board[y][x] += 1
                if y != 0 and board[y-1][x] == "X": #bottom
                    board[y][x] += 1
                if y != len(board)-1 and board[y+1][x] == "X": #top
                    board[y][x] += 1

                # checks for mines diagonally
                if y != len(board)-1 and x != 0 and board[y+1][x-1] == "X": #topLeft
                    board[y][x] += 1
                if y != len(board)-1 and x != len(board)-1 and board[y+1][x+1] == "X": #topRight
                    board[y][x] += 1
                if y != 0 and x != 0 and board[y-1][x-1] == "X": #bottomLeft
                    board[y][x] += 1
                if y != 0 and x != len(board)-1 and board[y-1][x+1] == "X": #bottomRight
                    board[y][x] += 1
            else:
                continue

def winCheck(cover, difficulty): # Checks each index of board, compares the amount of # symbols there are currently with how many there should be. If the two values are equal, it returns True.
    coverSize = len(cover)
    tileCount = 0
    for y in range(coverSize):
        for x in range(coverSize):
            if cover[y][x] != "#":
                tileCount += 1
    if tileCount == (coverSize ** 2) - (coverSize * 1):
        return True
    else:
        return False

def zeroClear(board, cover, y, x, count):
    boardSize = len(board)
    count -= 1 # This integer limits how much this function recurs. Recursion error without it.
    outOfBound = boundriesCheck(board, y, x)
    if outOfBound == False and board[y][x] != 0:
        cover[y][x] == board[y][x]
    elif count > 0 and outOfBound == False:
        if x != len(board)-1 and board[y][x+1] != "X": #right
            cover[y][x+1] = board[y][x+1]
            zeroClear(board, cover, y, x+1, count)
        if x != 0 and board[y][x-1] != "X": #left
            cover[y][x-1] = board[y][x-1]
            zeroClear(board, cover, y, x-1, count)
        if y != 0 and board[y-1][x] != "X": #bottom
            cover[y-1][x] = board[y-1][x]
            zeroClear(board, cover, y-1, x, count)
        if y != len(board)-1 and board[y+1][x] != "X": #top
            cover[y+1][x] = board[y+1][x]
            zeroClear(board, cover, y+1, x, count)

def boundriesCheck(board, y, x): # Checks to see if y and x are within the array
    boardSize = len(board)
    oob = False
    if x < 0:
        oob = True
    if y < 0:
        oob = True
    if x > boardSize - 1:
        oob = True
    if y > boardSize - 1:
        oob = True

    if oob == True:
        return True
    else:
        return False;

# PLAYER INTERACTION
def chooseTile(board, cover): # Lets the player choose a tile to reveal, if its a mine it returns true, else false.
    usryn = "n"
    while usryn == "n":
        try:
            print ("Please choose x coordinate: ", end="")
            x = int(input())
            print ("Please choose y coordinate: ", end="")
            y = int(input())
        except ValueError:

            continue
        usryn = yesOrNo("Are you sure of those coordinates(Y/n)?")

    # Tests the chosen value to see if it a mine or not.
    yInv = len(board) - y - 1 # y must be inverted for proper behavior
    usrCoords = board[yInv][x]
    if usrCoords == "X":
        return True
    elif usrCoords == 0:
        cover[yInv][x] = usrCoords
        zeroClear(board, cover, yInv, x, 10) # This last integer limits how much this function recurs itself. Limitation of python.
        return False
    else:
        cover[yInv][x] = usrCoords
        return False

def yesOrNo(message):
    while True:
        print(message, end="")
        usrIn = input()
        print("")
        if usrIn == "y":
            break
        elif usrIn == "n":
            break
        elif usrIn == "":
            break
        else:
            print("That is not y or n")
    return usrIn

# EXECUTABLE CODE
main()
