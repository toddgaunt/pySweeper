#! /usr/bin/python3
# author: Todd Gaunt
# apache 2.0
# minesweeper game

import random
import os
import curses

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

class Board(object):
    """This Board object contains Cell objects withing a list to act as the minesweeper game board"""
    def __init__(self, size=10):
        self.size = size
        self.brd = []
        for y in range(self.size):
            self.brd.append([])
            for x in range(self.size):
                cell = Cell()
                self.brd[y].append(cell)

    def print_cell(self, y=0, x=0):
        # retrieves the Cell from the array and prints it's tile variable
        cur_cell = self.brd[y][x]
        cur_tile = cur_cell.get_tile()
        print (str(cur_tile) + " ", end="")

    def print_brd(self):
        # loops through entire array and prints each Cell objects tile variable, if its revealed. Otherwise uses "#"
        count = self.size - 1
        for y in range(self.size):
            print (str(count) + " - " , end="")
            for x in range(self.size):
                cur_cell = self.brd[y][x]
                #cur_cell.show() uncomment to reveal all tiles
                if cur_cell.revealed == True:
                    cur_tile = cur_cell.get_tile()
                    print (str(cur_tile) + " ", end="")
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
            if cur_cell.get_tile() == "X":
                continue
            else:
                cur_cell.set_tile(True, "X")
                count -= 1

def main():
    mine_brd = Board()
    mine_brd.print_brd()
    mine_brd.plant_mines()
    mine_brd.print_brd()

if __name__ == "__main__":
    main()
