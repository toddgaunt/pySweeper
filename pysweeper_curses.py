#! /usr/bin/python3
# author: Todd Gaunt
# apache 2.0
# minesweeper game

from pysweeper import Board, Cell
from curses import wrapper
import curses
import time
import re
#TODO Refactor to make cleaner
#TODO extend curses windows class to enable window naming, so its easy to lookup window without
# caring about it's index number

class AppUI(object):
    def __init__(self, stdscr):
        # Initial variables
        self.menu = True
        self.playing = False
        self.win = False
        self.win_counter = 0
        self.loss_counter = 0
        self.game_time = 0
        self.windows = {}
        self.sub_windows = {}

        # Main window
        self.stdscr = stdscr

        # Sets initial terminal properties
        self.stdscr.clear()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        if curses.has_colors():
            curses.start_color()

        # Sets Color pairs for curses to use (fg, bg)
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)

        #self.refresh_windows()

    def board_window(self):
        # Draws the board_window
        self.windows.update({"board": curses.newwin(curses.LINES-4, curses.COLS,1,0)})
        self.sub_windows.update({"board": curses.newwin(curses.LINES-7, curses.COLS-3, 2, 2)})
        self.windows["board"].box()
        self.add_brd_str(self.sub_windows["board"])

    def prompt_window(self):
        # Draws prompt_window
        self.windows.update({"prompt": curses.newwin(3, curses.COLS, curses.LINES-3, 0)})
        self.sub_windows.update({"prompt": curses.newwin(1, curses.COLS-4, curses.LINES-2,2)})
        self.windows["prompt"].box()
        self.prompt_message(self.sub_windows["prompt"])

    def title_window(self):
        # Draws title_window
        self.windows.update({"title": curses.newwin(1, curses.COLS, 0, 0)})
        self.windows["title"].clear()
        self.windows["title"].addstr("Pysweeper 2.0", curses.A_REVERSE)
        self.windows["title"].chgat(-1, curses.A_REVERSE)

    def prompt_message(self, window):
        """Depending on class variables menu, playing, and game_over, different prompts
        are displayed, calls info_message and get_coords to do so."""
        #if self.playing:
        #    self.get_coords(window)
        if False:
            pass
        elif self.menu:
            window.clear()
            window.addstr(0,0, "Press r to start the game, q to quit.")
            window.chgat(0,0,curses.COLS-4,curses.color_pair(4))
        else:
            self.info_message(window)

    def info_message(self, window):
        window.clear()
        window.addstr("Win = {}. You have {} wins and {} losses.".format(self.win, self.win_counter, self.loss_counter))
        window.refresh()

    def get_coords(self, window, board):
        """Catches String input from user, and returns a list with 3 groups, (x)(y)(f)."""
        xyf = re.compile(r"([0-9]+),([0-9]+)(f?)")
        while True:
            window.clear()
            window.addstr(0,0, "Enter x and y coordinates: x,y")
            window.chgat(0,0,curses.COLS-4, curses.color_pair(3))
            # Takes string for coordinates
            curses.echo()
            caught_str=""
            while True:
                caught_str += window.getstr(0,27).decode(encoding="utf-8")
            curses.noecho()
            window.refresh()
            # Compares against regex
            re_match = xyf.match(str(caught_str))
            # If no match, print error message
            if re_match == None:
                window.clear()
                window.addstr(0,0,"Not a coordinate (Press any key to continue).")
                window.chgat(0,0,curses.COLS-4, curses.color_pair(2) | curses.A_REVERSE)
                window.refresh()
                window.getch()
                continue
            # If coordinates are out of bounds, print error message
            elif int(re_match.group(1)) >= board.x_length or int(re_match.group(2)) >= board.y_length:
                window.clear()
                window.addstr(0,0,"Coordinates are out of bounds (press any key to continue).")
                window.chgat(0,0,curses.COLS-4, curses.color_pair(2) | curses.A_REVERSE)
                window.refresh()
                window.getch()
                continue
            # If every test is passed, modify the board coordinates as a 3-index list
            else:
                window.clear()
                window.addstr(0,0,re_match.group(0) + " are valid coordinates")
                window.chgat(0,0,curses.COLS-4, curses.color_pair(3))
                window.refresh()
                coords = []
                coords.append(re_match.group(1))
                coords.append(re_match.group(2))
                coords.append(re_match.group(3))
                return coords

    def parse_coords(self, coords, board):
        x = int(coords[0])
        y = int(coords[1])
        if coords[2] == 'f':
            board[y][x].flag()
        else:
            # flip_cell() returns True if the cell is a mine
            if board.flip_cell(y,x):
                return True
        return False

    def add_brd_str(self, window):
        """Displays all cells of the array into a curses window"""
        board = self.mine_brd
        if self.playing:
            window.clear()
            y_flip = board.y_length - 1
            for y in range(board.y_length):
                window.addstr(y, 0, str(y_flip) + "-" )
                for x in range(board.x_length):
                    if board[y_flip][x].revealed:
                        tilech = board[y_flip][x].tile
                        if tilech == 'X':
                            tile_color = 2
                        elif tilech == "0":
                            tile_color = 1
                        elif tilech == "1":
                            tile_color = 4
                        elif tilech == "2":
                            tile_color = 3
                        else:
                            tile_color = 5
                    elif board[y_flip][x].flagged == True:
                        tilech = "f"
                        tile_color = 1
                    else:
                        tilech = "#"
                        tile_color = 1
                    window.addstr(y, 2 + (x*2), str(tilech), curses.color_pair(tile_color))
                y_flip -= 1
            for x in range(board.x_length):
                window.addstr(1 + y, 2 + (x * 2), "|")
                window.addstr(2 + y, 2 + (x * 2), str(x))
        else:
            pass

    def make_board(self):
        self.mine_brd = Board()
        self.mine_brd.plant_mines()
        self.mine_brd.count_surrounding()
        for y in range(self.mine_brd.y_length):
            for x in range(self.mine_brd.x_length):
                self.mine_brd[y][x].revealed=True

    def update_stats(self):
        """Updates all game stats"""
        if self.win == True:
            self.win_counter += 1
        elif self.win == False:
            self.loss_counter += 1

    def refresh_windows(self):
        y, x = self.stdscr.getmaxyx()
        curses.resize_term(y, x)
        curses.KEY_RESIZE
        self.stdscr.noutrefresh()

        self.title_window()
        self.prompt_window()
        self.board_window()

        for i in self.windows:
            self.windows[i].noutrefresh()

        for i in self.sub_windows:
            self.sub_windows[i].noutrefresh()

        curses.doupdate()

    def restore_term(self):
        """Restore terminal settings"""
        curses.nocbreak()
        curses.echo()
        curses.curs_set(1)

        # Ends curses
        curses.endwin()

def main(stdscr):
    UI = AppUI(stdscr)
    UI.playing = True
    UI.make_board()
    while True:
        UI.refresh_windows()
        UI.stdscr.getch()
    # End of program
    UI.restore_term()

if __name__ == "__main__":
    """Curses wrapper lets me debug without fucking up terminal windows"""
    wrapper(main)
