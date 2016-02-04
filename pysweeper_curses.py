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

        # Interal windows and pads
        self.brdwin = curses.newwin(30, 30, 0, 0) #height, width, y, x
        self.estwin = curses.newwin(15, 30, 0, 30) #height, width, y, x
        self.sthwin = curses.newwin(30, 15, 30, 0) #height, width, y, x

    def kill(self):
        # Kills main window
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    def south_window(self):
        self.sthwin.addstr("hello")
        self.sthwin.refresh()

    def east_window(self):
        self.estwin.addstr("hello")
        self.estwin.refresh()

    def help_menu(self):
        pass

    def board_window(self):
        self.brdwin.addstr("hello")
        self.brdwin.refresh()

def main(stdscr):
    gui = appGUI(stdscr)
    gui.board_window()
    gui.south_window()
    gui.east_window()
    time.sleep(10)
    gui.kill()


if __name__ == "__main__":
   curses.wrapper(main)
