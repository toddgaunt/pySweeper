#! /usr/bin/python3
# author: Todd Gaunt
# apache 2.0
# minesweeper game

from pysweeper import Board, Cell
from curses import wrapper
import curses
import time

def main(stdscr):
    #stdscr = curses.initscr()
    stdscr.clear()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)

    # Allows terminals without color to function
    if curses.has_colors():
        curses.start_color()

    # Color pairs (fg, bg)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)

    # Adds title and then colors whole line
    stdscr.addstr("Pysweeper 1.0", curses.A_REVERSE)
    stdscr.chgat(-1, curses.A_REVERSE)

    # Adds menu at bottom
    text_window = curses.newwin(3,curses.COLS,curses.LINES-3,0)
    text_window.addstr(1,2, "Press r to start the game, q to quit.")
    text_window.chgat(1,2,curses.COLS-4,curses.color_pair(3) | curses.A_REVERSE)
    text_window.box()

    # Main window for holding the game board
    game_window = curses.newwin(curses.LINES-4,curses.COLS,1,0)

    # Subwindow for the game board that makes updating clean
    game_board_window = game_window.subwin(curses.LINES-6, curses.COLS-3, 2,2)

    # Inital text for subwindow
    game_board_window.addstr("Game goes here.")

    # Draws a border around the main window
    game_window.box()

    # Update internal window data structures
    stdscr.noutrefresh()
    game_window.noutrefresh()
    text_window.noutrefresh()

    # Redraw the screen
    curses.doupdate()

    playing = True
    while playing:
        player_input = game_window.getch()

        if player_input == ord('r') or player_input == ord('R'):

            # Inializes game board
            mine_brd = Board()
            mine_brd.plant_mines()
            mine_brd.count_surrounding()

            # Generation message
            game_board_window.clear()
            game_board_window.addstr('You pressed r, adding game board.', curses.color_pair(3))
            game_board_window.refresh()
            time.sleep(1)

            # Some debugging code
            for y in range(mine_brd.y_length):
                for x in range(mine_brd.x_length):
                    mine_brd.flip_cell(y,x)

            # Adds the actual tiles of the board to the window
            game_board_window.clear()
            add_brd_str(mine_brd, game_board_window)
            game_board_window.refresh()
            get_coords(text_window)

        elif player_input == ord('q') or player_input == ord('Q'):
            playing = False

        # Refresh the windows from the bottom up
        stdscr.noutrefresh()
        game_window.noutrefresh()
        game_board_window.noutrefresh()
        curses.doupdate()

    # End of program
    restore_term()

def get_coords(window):
    window.clear
    window.addstr(1,2, "Enter x and y coordinates: ")
    window.chgat(1,2,curses.COLS-4, curses.color_pair(2) | curses.A_REVERSE)
    coords = window.getstr()
    window.refresh

def add_brd_str(board, window):
    """Displays all cells of the array into a curses window"""
    y_flip = board.y_length - 1
    for y in range(board.y_length):
        window.addstr(y + (curses.LINES//6), (curses.COLS//3), str(y_flip) + "-" )
        for x in range(board.x_length):
            if board.get_cell(y_flip,x).revealed:
                tile = board.get_cell(y_flip,x).get_tile()
            elif board.get_cell(y_flip,x).flagged == True:
                tile = "f"
            else:
                tile = "#"

            if tile == "X":
                tile_color = 1
            elif tile == 1:
                tile_color = 2
            elif tile >= 2:
                tile_color = 3
            else:
                tile_color = 4
            window.addstr(y + (curses.LINES//6),
                          2 + (x * 2) + (curses.COLS//3),
                          str(tile),
                          curses.color_pair(tile_color))

        y_flip -= 1
    for x in range(board.x_length):
        window.addstr(1 + y + (curses.LINES//6), 2 + (x * 2) + (curses.COLS//3), "|")
        window.addstr(2 + y + (curses.LINES//6), 2 + (x * 2) + (curses.COLS//3), str(x))

def restore_term():
    # Restore terminal settings
    curses.nocbreak()
    curses.echo()
    curses.curs_set(1)

    # Ends curses
    curses.endwin()

if __name__ == "__main__":
    # Curses wrapper lets me debug without fucking up terminal windows
    wrapper(main)
