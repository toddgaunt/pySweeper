#! /usr/bin/python3
# author: Todd Gaunt
# apache 2.0
# minesweeper game

import pysweeper
import curses

class pyCurses(curses.initscr()):
    def __init__(self):
        #curses.noecho()
        #curses.cbreak()
        #self.keypad(1)

    def kill(self):
        curses.nocbreak()
        self.keypad(0)
        curses.echo()
        curses.endwin()
    def say_hello():
        print ("hello")


def main():
    stdscr = pyCurses()
    #stdscr.kill()
    stdscr.say_hello()

if __name__ == "__main__":
    main()
