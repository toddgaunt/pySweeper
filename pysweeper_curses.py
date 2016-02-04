#! /usr/bin/python3
# author: Todd Gaunt
# apache 2.0
# minesweeper game

from pysweeper import Board, Cell
import curses
import time

def main():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)

    if curses.has_colors():
        curses.start_color()

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)

    # Adds title and then colors whole line
    stdscr.addstr("Pysweeper 1.0", curses.A_REVERSE)
    stdscr.chgat(-1, curses.A_REVERSE)

    # Adds menu at bottom
    stdscr.addstr(curses.LINES-1,0, "Press r to start the game, q to quit.")
    stdscr.chgat(curses.LINES-1,7,1,curses.A_BOLD | curses.color_pair(2))

    # Main window for holding the game board
    game_window = curses.newwin(curses.LINES-2,curses.COLS,1,0)

    # Subwindow for the game board that makes updating clean
    game_board_window = game_window.subwin(curses.LINES-6, curses.COLS-4, 3,3)

    # Inital text for subwindow
    game_board_window.addstr("Game goes here.")

    # Draws a border around the main window
    game_window.box()

    # Update internal window data structures
    stdscr.noutrefresh()
    game_window.noutrefresh()

    # Redraw the screen
    curses.doupdate()

    while True:
        player_input = game_window.getch()

        if player_input == ord('r') or player_input == ord('R'):
            mine_brd = Board()
            mine_brd.plant_mines()
            mine_brd.count_surrounding()
            for y in range(mine_brd.y_length):
                for x in range(mine_brd.x_length):
                    mine_brd.flip_cell(y,x)

            game_board_window.clear()
            game_board_window.addstr('You pressed r, adding game board.', curses.color_pair(3))
            game_board_window.refresh()
            game_board_window.clear()
            time.sleep(1)
            game_board_window.addstr(mine_brd.print_brd())

        elif player_input == ord('q') or player_input == ord('Q'):
            break

        # Refresh the windows from the bottom up
        stdscr.noutrefresh()
        game_window.noutrefresh()
        game_board_window.noutrefresh()
        curses.doupdate()

    # End of program
    restore_term()

def restore_term():
    # Restore terminal settings
    curses.nocbreak()
    curses.echo()
    curses.curs_set(1)

    # Ends curses
    curses.endwin()

if __name__ == "__main__":
    # If there are any exceptions, don't break the terminal!
    try:
        main()
    except:
        restore_term()
