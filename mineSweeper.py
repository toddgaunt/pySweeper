#! /usr/bin/python3
# author: Todd Gaunt
# apache 2.0
# minesweeper game

import random
import os
import curses

#TODO implement object oriented minesweeper

class cell(object):
    def __init__(self, mine, revealed=False, tagged=False):
        self.mine = mine
        self.revealed = revealed
        self.tag = tag

    def show(self):
        self.revealed = True

    def flag(self):
        self.tag = not self.tag

    def set_mine(self):
        self.mine = True

class board(list):

def main():


if __name__ == "__main__":
    main()
