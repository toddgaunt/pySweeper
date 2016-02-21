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
    def __init__(self, stdscr, playing=True, win=False, win_counter=0, loss_counter=0, game_time=0):
        # Initial variables
        self.playing = True
        self.win = False
        self.win_counter = 0
        self.loss_counter = 0
        self.game_time = 0
        self.windows = []
        self.sub_windows = []

        # Creating UI windows
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

        # Draws all main windows
        self.draw_windows()

    def create_window(self, nlines, ncols, beginy, beginx):
        """Function that creates a curses.window object and appends it to an array of windows"""
        self.windows.append(curses.newwin(nlines, ncols, beginy, beginx))

    def create_sub_window(self, window, nlines, ncols, beginy, beginx):
        """Function that creates a window.sub_window object and appends it to an array of sub windows"""
        self.sub_windows.append(self.windows[window].subwin(nlines, ncols, beginy, beginx))

    def title_message(self, window):
        # Adds title and then colors whole line to top of stdscr
        window.addstr("Pysweeper 1.1", curses.A_REVERSE)
        window.chgat(-1, curses.A_REVERSE)

    def prompt_message(self, window):
        """Prompts the user to start playing, and returns a character they input"""
        window.clear()
        window.addstr(0,0, "Press r to start the game, q to quit.")
        window.chgat(0,0,curses.COLS-4,curses.color_pair(4))
        window.refresh()
        return window.getch()

    def info_message(self, window):
        window.clear()
        window.addstr("\nWin = {}. You have {} wins and {} losses.".format(self.win, self.win_counter, self.loss_counter))
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
            caught_str = window.getstr(0,27).decode(encoding="utf-8")
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

    def add_brd_str(self, window, board):
        """Displays all cells of the array into a curses window"""
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
        window.refresh()

    def update_stats(self):
        """Updates all game stats"""
        if self.win == True:
            self.win_counter += 1
        elif self.win == False:
            self.loss_counter += 1

    def draw_windows(self):
        """Refreshes all window in class from the bottom up"""
        """ Contains predfined properties of main UI windows"""
        # Resizes windows to term size
        y, x = self.stdscr.getmaxyx()
        curses.resize_term(y, x)
        curses.KEY_RESIZE

        # Resets window arrays
        self.windows = []
        self.sub_windows = []

        # Board window and sub window
        self.create_window(curses.LINES-4, curses.COLS,1,0)
        self.create_sub_window(0, curses.LINES-7, curses.COLS-3, 2, 2)
        self.windows[0].box()

        # Text window and sub window
        self.create_window(3, curses.COLS, curses.LINES-3, 0)
        self.create_sub_window(1, 1, curses.COLS-4, curses.LINES-2,2)
        self.windows[1].box()

        # Window for holding title
        self.create_window(1, curses.COLS, 0, 0)

        # draws title message
        self.title_message(self.windows[2])

        # Update internal window data structures
        for i in range(len(self.windows)):
            self.windows[i].noutrefresh()
        for i in range(len(self.sub_windows)):
            self.sub_windows[i].noutrefresh()

        # Redraws the screen
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
    while UI.playing:
        player_input = UI.prompt_message(UI.sub_windows[1])
        if player_input == ord('r') or player_input == ord('R'):
            # Initializes board
            mine_brd = Board()

            # Board generation message
            UI.sub_windows[0].clear()
            UI.sub_windows[0].addstr('Generating a board with {} length and {} height with {} mines.'.format(mine_brd.x_length, mine_brd.y_length, mine_brd.mined_tiles), curses.color_pair(3))
            UI.sub_windows[0].refresh()
            time.sleep(1)

            # Initializes screen with game board
            # Doesn't plant any mines or increment tiles until first coordinate has been chosen
            UI.add_brd_str(window=UI.sub_windows[0], board=mine_brd)
            coords = UI.get_coords(window=UI.sub_windows[1], board=mine_brd)
            # Marks the cell as selected so that the plant_mines() function won't plant a mine there
            mine_brd[int(coords[1])][int(coords[0])].selected = True
            mine_brd.plant_mines()
            mine_brd.count_surrounding()
            game_over = UI.parse_coords(coords, mine_brd)
            game_over = False
            # prints board to curses window, then calls function to grab user input
            while True:
                UI.draw_windows()
                UI.add_brd_str(window=UI.sub_windows[0], board=mine_brd)
                coords = UI.get_coords(window=UI.sub_windows[1], board=mine_brd)
                game_over = UI.parse_coords(coords, mine_brd)
                if game_over:
                    break
            # Increments wins and losses
            UI.update_stats()
            # Prints game info to player after game is over
            UI.info_message(UI.sub_windows[0])
            time.sleep(1)

        elif player_input == ord('q') or player_input == ord('Q'):
            UI.playing = False

        UI.draw_windows()
    # End of program
    UI.restore_term()

if __name__ == "__main__":
    """Curses wrapper lets me debug without fucking up terminal windows"""
    wrapper(main)
