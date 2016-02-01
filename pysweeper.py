#! /usr/bin/python3
# author: Todd Gaunt
# apache 2.0
# minesweeper game

import random
#import os
#import curses

#TODO implement object oriented minesweeper

class Cell(object):
    """Is a single cell of the minesweeper board"""
    def __init__(self, mine=False, revealed=False, tag=False, tile=0):
        self.mine = mine #
        self.revealed = revealed # whether or not the player can see the tile
        self.tag = tag # whether or not the player marked the tile
        self.tile = tile # the character used to represent the tile

    def show(self):
        self.revealed = True

    def flag(self):
        self.tag = not self.tag

    def get_tile(self):
        return self.tile

    def set_tile(self, mine=False, tile=0):
        self.tile = tile
        self.mine = mine

    def increment_tile(self):
        if self.tile != "X":
            self.tile += 1

class Board(object):
    """This Board object contains Cell objects withing a list to act as the minesweeper game board"""
    def __init__(self, size=10, mine_count=0, revealed_tiles=0):
        self.size = size
        self.mine_count = mine_count
        self.revealed_tiles = revealed_tiles
        self.brd = []
        for y in range(self.size):
            self.brd.append([])
            for x in range(self.size):
                cell = Cell()
                self.brd[y].append(cell)

    def print_brd(self):
        # loops through entire array and prints each Cell objects tile variable, if its revealed. Otherwise uses "#"
        count = self.size - 1
        for y in range(self.size):
            print (str(count) + " - " , end="")
            for x in range(self.size):
                current_cell = self.brd[count][x]
                if: current_cell.revealed == True:
                    print (str(current_cell.get_tile()) + " ", end="")
                else:
                    print ("# ", end="")
            count -= 1
            print("")
        count = 0
        print("    ", end="")
        print("| " * self.size)
        print("    ", end="")
        for i in range(self.size):
            print(str(count) + " ", end="")
            count += 1
        print("")

    def plant_mines(self):
        count = self.size
        while count > 0:
            y = random.randint(0, self.size -1)
            x = random.randint(0, self.size -1)
            cur_cell = self.brd[y][x]
            if cur_cell.get_tile() == "X" or cur_cell.revealed:
                continue
            else:
                cur_cell.set_tile(True, "X")
                self.mine_count += 1
                count -= 1

    def count_surrounding(self):
        coordinates = [[-1, -1], [-1, 0], [-1, 1],
                       [0 , -1],          [0 , 1],
                       [1 , -1], [1 , 0], [1 , 1]]
        for y in range(self.size):
            for x in range(self.size):
                if self.brd[y][x].get_tile() == "X":
                    for i in range(len(coordinates)):
                        y_offset = y+coordinates[i][0]
                        x_offset = x+coordinates[i][1]
                        if y_offset < 0 or y_offset >= self.size or x_offset >= self.size or x_offset < 0:
                            continue
                        self.brd[y_offset][x_offset].increment_tile()

    def cell_flip(self, y, x):
        x = int(x)
        y = int(y)
        self.brd[y][x].show()
        if self.brd[y][x].get_tile() == "X":
            self.revealed_tiles += 1
            return True
        else:
            self.revealed_tiles += 1
            return False

    def get_cell(self, y=0, x=0):
        return self.brd[y][x]

def main():
    mine_brd = Board()
    mine_brd.print_brd()
    coords = get_coords()
    mine_brd.cell_flip(coords[0], coords[1])
    mine_brd.plant_mines()
    mine_brd.count_surrounding()
    game_over = False
    win = False
    while game_over == False:
        mine_brd.print_brd()
        coords = get_coords()
        game_over =  mine_brd.cell_flip(coords[0], coords[1])
        if mine_brd.size * mine_brd.size - mine_brd.mine_count == mine_brd.revealed_tiles:
            game_over = True
            win = True
    if win == True:
        print ("You win!")
    else:
        print ("You lose...")
def get_coords():
    print("Please enter x-coordinate")
    x = input()
    print("Please enter y-coordinate")
    y = input()
    coords = [y,x]
    return coords

if __name__ == "__main__":
    main()