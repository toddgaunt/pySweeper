#! /usr/bin/python3
# author: Todd Gaunt
# apache 2.0
# minesweeper game

from pysweeper import Board, Cell
import curses
import time

class appGUI():
    def __init__(self, stdscr):
        """Draws all main windows the program uses"""
        # Initialize class variables and assign stdscr
        self.stdscr = stdscr

        # Actually creating minesweeper board
        self.mine_brd = Board()
        self.mine_brd.plant_mines()
        self.mine_brd.count_surrounding()

        # Creates main window
        self.stdscr.clear()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)

    def kill(self):
        # Kills main window
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    def brdscr(self):
        begin_x = 20; begin_y = 7
        height = 100; width = 100
        brdscr = curses.newwin(height, width, begin_y, begin_x)

        for y in range(self.mine_brd.y_length):
            for x in range(self.mine_brd.x_length):
                self.mine_brd.cell_flip(y, x)
                brdscr.addstr(self.mine_brd.print_brd())
                brdscr.refresh()
                brdscr.erase()

def main(stdscr):
    gui = appGUI(stdscr)
    gui.brdscr()
    time.sleep(10)
    gui.kill()


if __name__ == "__main__":
   curses.wrapper(main)

