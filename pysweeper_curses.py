#! /usr/bin/python3
# author: Todd Gaunt
# apache 2.0
# minesweeper game

from pysweeper import Board, Cell
from curses import wrapper
import curses
import time
import re

#TODO, refactor main() into a class so that the game can be expanded to multiple boards being played

def main(stdscr):
    """Main loop for gameplay"""
    # Initial variables
    win_counter = 0
    loss_counter = 0
    playing = True

    # Sets initial terminal properties
    stdscr.clear()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    if curses.has_colors():
        curses.start_color()

    # Sets Color pairs (fg, bg)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    # Adds title and then colors whole line
    stdscr.addstr("Pysweeper 1.0", curses.A_REVERSE)
    stdscr.chgat(-1, curses.A_REVERSE)

    # Adds menu at bottom
    # subwindow makes updating clean
    text_window = curses.newwin(3,curses.COLS,curses.LINES-3,0)
    text_window.box()
    text_sub_window = text_window.subwin(1, curses.COLS-4, curses.LINES-2,2)

    # Main window for holding the game board
    # subwindow makes updating clean
    game_window = curses.newwin(curses.LINES-4,curses.COLS,1,0)
    game_window.box()
    game_board_window = game_window.subwin(curses.LINES-6, curses.COLS-3, 2,2)

    # Update internal window data structures
    stdscr.noutrefresh()
    game_window.noutrefresh()
    text_window.noutrefresh()

    # Redraw the screen
    curses.doupdate()

    while playing:
        text_sub_window.clear()
        text_sub_window.addstr(0,0, "Press r to start the game, q to quit.")
        text_sub_window.chgat(0,0,curses.COLS-4,curses.color_pair(4))
        text_sub_window.refresh()
        player_input = game_window.getch()

        if player_input == ord('r') or player_input == ord('R'):
            # Initializes board
            mine_brd = Board()

            # Generation message
            game_board_window.clear()
            game_board_window.addstr('Generating a board with {} length and {} height with {} mines.'.format(mine_brd.x_length, mine_brd.y_length, mine_brd.mine_count), curses.color_pair(3))
            game_board_window.refresh()
            time.sleep(1)

            # asks for first coordinate to prevent first selection
            # from being a mine, then plants mines and increments the tiles
            add_brd_str(window=game_board_window, board=mine_brd)
            get_coords(window=text_sub_window, board=mine_brd)
            mine_brd.plant_mines()
            mine_brd.count_surrounding()

            game_over = False
            win = False
            # prints board to curses window, then calls function to grab user input
            while True:
                add_brd_str(window=game_board_window, board=mine_brd)
                game_over = get_coords(window=text_sub_window, board=mine_brd)
                if game_over:
                    break
                elif mine_brd.y_length * mine_brd.x_length - mine_brd.mine_count == mine_brd.revealed_tiles:
                    win = True
                    break
            # Increments wins and losses
            if win == True:
                win_counter += 1
            elif win == False:
                loss_counter += 1
            # Prints game info to player after game is over
            add_game_info(game_board_window, win, win_counter, loss_counter)

        elif player_input == ord('q') or player_input == ord('Q'):
            playing = False

        # Refresh the windows from the bottom up
        stdscr.noutrefresh()
        game_window.noutrefresh()
        game_board_window.noutrefresh()
        text_window.noutrefresh()
        text_sub_window.noutrefresh()
        curses.doupdate()

    # End of program
    restore_term()

def get_coords(window, board):
    """regex for seperating coordinates and f flag into groups"""
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
        # Compares
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
            break

    x = int(coords[0])
    y = int(coords[1])

    if coords[2] == 'f':
        board[y][x].flag()
    else:
        board.flip_cell(y,x)
        if board[y][x].mine:
            return True
    return False

def add_brd_str(window, board):
    """Displays all cells of the array into a curses window"""
    window.clear()
    y_flip = board.y_length - 1
    for y in range(board.y_length):
        window.addstr(y, 0, str(y_flip) + "-" )
        for x in range(board.x_length):
            if board.get_cell(y_flip,x).revealed:
                tile = board.get_cell(y_flip,x).get_tile()
                if tile == 'X':
                    tile_color = 2
                elif tile == 0:
                    tile_color = 1
                elif tile == 1:
                    tile_color = 4
                elif tile == 2:
                    tile_color = 3
                else:
                    tile_color = 5
            elif board.get_cell(y_flip,x).flagged == True:
                tile = "f"
                tile_color = 1
            else:
                tile = "#"
                tile_color = 1
            window.addstr(y, 2 + (x*2), str(tile), curses.color_pair(tile_color))

        y_flip -= 1
    for x in range(board.x_length):
        window.addstr(1 + y, 2 + (x * 2), "|")
        window.addstr(2 + y, 2 + (x * 2), str(x))
    window.refresh()

def add_game_info(window, win, win_counter, loss_counter):
    """Adds game information string to desired window"""
    window.clear()
    window.addstr("Win = {}. You have {} wins and {} losses.".format(win, win_counter, loss_counter))
    window.refresh()

def restore_term():
    """Restore terminal settings"""
    curses.nocbreak()
    curses.echo()
    curses.curs_set(1)

    # Ends curses
    curses.endwin()

if __name__ == "__main__":
    """Curses wrapper lets me debug without fucking up terminal windows"""
    wrapper(main)


""" Unused functions
    def add_brd_str_centered(board, window):
        window.clear()
        #Displays all cells of the array into a curses window
        y_flip = board.y_length - 1
        for y in range(board.y_length):
            window.addstr(y + (curses.LINES//6), (curses.COLS//3), str(y_flip) + "-" )
            for x in range(board.x_length):
                if board.get_cell(y_flip,x).revealed:
                    tile = board.get_cell(y_flip,x).get_tile()
                    if tile == 'X':
                        tile_color = 2
                    elif tile == 0:
                        tile_color = 1
                    elif tile == 1:
                        tile_color = 4
                    elif tile == 2:
                        tile_color = 3
                    else:
                        tile_color = 5
                elif board.get_cell(y_flip,x).flagged == True:
                    tile = "f"
                    tile_color = 1
                else:
                    tile = "#"
                    tile_color = 1
                window.addstr(y + (curses.LINES//6),
                              2 + (x * 2) + (curses.COLS//3),
                              str(tile),
                              curses.color_pair(tile_color))

            y_flip -= 1
        for x in range(board.x_length):
            window.addstr(1 + y + (curses.LINES//6), 2 + (x * 2) + (curses.COLS//3), "|")
            window.addstr(2 + y + (curses.LINES//6), 2 + (x * 2) + (curses.COLS//3), str(x))
        window.refresh()
    """
