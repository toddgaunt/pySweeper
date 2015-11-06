#! /usr/bin/python3
# author: Todd Gaunt
# apache 2.0
# minesweeper game

import random
import os
import curses

#TODO implement object oriented minesweeper

class Cell(object):
    "Is a single cell of the minesweeper board"
    def __init__(self, mine=False, revealed=False, tag=False, tile=0):
        self.mine = mine
        self.revealed = revealed
        self.tag = tag
        self.tile = tile

    def show(self):
        self.revealed = True

    def flag(self):
        self.tag = not self.tag

    def set_mine(self):
        self.mine = True
        self.tile = "X"

    def get_tile(self):
        return self.tile

class Board(object):
    "The 2d array that acts as the minesweeper board"
    def __init__(self, size=10):
        self.size = size
        self.brd = []
        for y in range(self.size):
            self.brd.append([])
            for x in range(self.size):
                cell = Cell()
                self.brd[y].append(cell)

    def print_cell(self, y=0, x=0):
        cur_cell = self.brd[y][x]
        cur_tile = cur_cell.get_tile()
        print (str(cur_tile) + " ", end="")

    def print_brd(self):
        count = self.size - 1
        for y in range(self.size):
            print (str(count) + " - " , end="")
            for x in range(self.size):
                cur_cell = self.brd[y][x]
                cur_tile = cur_cell.get_tile()
                print (str(cur_tile) + " ", end="")
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
                cur_cell.set_mine()
                count -= 1

def main():
    mine_brd = Board()
    mine_brd.print_brd()
    mine_brd.plant_mines()
    mine_brd.print_brd()

if __name__ == "__main__":
    main()
