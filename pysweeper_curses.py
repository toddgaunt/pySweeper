#! /usr/bin/python3
# author: Todd Gaunt
# apache 2.0
# minesweeper game

from curses import wrapper
import curses
import random
#WARNING: This code is really shitty curses programming, tis how I learned not to use the library

class Cell(object):
    """Is a single cell of the minesweeper board"""
    def __init__(self, mine=False, revealed=False, flagged=False, selected=False, _tile=0):
        self.mine = mine # Whether or not there is a mine
        self.revealed = revealed # Whether or not the player can see the tile
        self.flagged = flagged # Whether or not the player marked the tile
        self.selected = selected # Whether or not the player has selected this tile
        self._tile = _tile # The character used to represent the tile

    def reveal(self):
        self.revealed = True

    def flag(self):
        """toggles flags on a tile"""
        self.flagged = not self.flagged

    @property
    def tile(self):
        """returns a string of the tile."""
        return str(self._tile)

    @tile.setter
    def tile(self, value):
        self._tile = value
        if value == "X":
            self.mine = True
        else:
            self.mine = False

    def increment_tile(self):
        """If the tile is not a mine, increment it by 1"""
        if not self.mine:
            self.tile = str(int(self.tile) + 1)

class Board(list):
    """This Board object contains Cell objects within itself to represent the minesweeper game board"""
    def __init__(self, x_length=10, y_length=10, mined_tiles=0, revealed_tiles=0, flagged_tiles=0):
        self.x_length = x_length
        self.y_length = y_length
        self.mtiles = mined_tiles
        self.rtiles = revealed_tiles
        self.ftiles = flagged_tiles
        for y in range(self.y_length):
            self.append([])
            for x in range(self.x_length):
                self[y].append(Cell())
        self.alltiles = y_length * x_length

    def plant_mines(self, diff):
        """Plants exactly the amount of mines according to algorithm"""
        count = (self.y_length * self.x_length / ((self.y_length + self.x_length) / (diff/2)))
        while count > 0:
            y = random.randint(0, self.y_length -1)
            x = random.randint(0, self.x_length -1)
            if self[y][x].mine or self[y][x].selected:
                continue
            else:
                self[y][x].tile = "X"# mine=True
                self.mtiles += 1
                count -= 1

    def count_surrounding(self):
        """Check surrounding tiles of mines and increments them if they are not a mine"""
        coordinates = [[-1, -1], [-1, 0], [-1, 1],
                       [0 , -1],          [0 , 1],
                       [1 , -1], [1 , 0], [1 , 1]]
        for y in range(self.y_length):
            for x in range(self.x_length):
                if self[y][x].tile == "X":
                    for i in range(len(coordinates)):
                        y_offset = y+coordinates[i][0]
                        x_offset = x+coordinates[i][1]
                        if y_offset < 0 or y_offset >= self.y_length or x_offset >= self.x_length or x_offset < 0:
                            continue
                        self[y_offset][x_offset].increment_tile()

    def flip_cell(self, y, x):
        """Reveals the tile according to x,y coordinates. If the tile
        is a mine returns True, else False. Auto_flips all 0s if a 0 is found"""
        coordinates = [[-1, 0],
               [0 , -1],      [0 , 1],
                       [1 , 0]]
        y = int(y)
        x = int(x)
        if self[y][x].revealed:
            return False

        # Reveals current cell
        self[y][x].reveal()
        self.rtiles += 1

        if self[y][x].mine:
            return True

        if self[y][x].tile == "0":
            for i in range(len(coordinates)):
                y_offset = y+coordinates[i][0]
                x_offset = x+coordinates[i][1]
                # Prevents out_of_bounds errors from happening
                if y_offset < 0 or y_offset >= self.y_length or x_offset >= self.x_length or x_offset < 0:
                    continue
                self.flip_cell(y_offset, x_offset)
        return False

    def flag_cell(self,y,x):
            self[y][x].flag()
            self.ftiles += 1


class AppUI(object):
    def __init__(self, stdscr):
        # Initial variables
        # This value tells the windows which messages to show. Values are "menu" "gamescr" and "options"
        self.prompt="menu"

        # Tracks if game should close or not
        self.playing = True

        # Option to reveal board
        self.revealed = False

        # Initial placeholder game board
        self.mine_brd = Board()

        # Some variables for tracking coordinates
        self.first_move=True
        self.toggle=True
        self.toggle2=True
        self.coords=[' ',' ',' ']

        # The coords the prompter displays
        self.fcrds=[' ',' ',' ']

        # Other vars
        self.board_size=10
        self.difficulty=4
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

        self.init_windows()

    def title_window(self):
        # Draws title_window
        self.windows.update({"title": curses.newwin(1, curses.COLS, 0, 0)})
        self.windows["title"].clear()
        self.windows["title"].addstr("Pysweeper 2.0", curses.A_REVERSE)
        self.windows["title"].chgat(-1, curses.A_REVERSE)

    def board_window(self):
        # Draws the board_window
        self.windows.update({"board": curses.newwin(curses.LINES-4, curses.COLS,1,0)})
        self.sub_windows.update({"board": curses.newwin(curses.LINES-7, curses.COLS-3, 2, 2)})
        self.windows["board"].box()

    def prompt_window(self):
        # Draws prompt_window
        self.windows.update({"prompt": curses.newwin(3, curses.COLS, curses.LINES-3, 0)})
        self.sub_windows.update({"prompt": curses.newwin(1, curses.COLS-4, curses.LINES-2,2)})
        self.windows["prompt"].box()

    def prompt_message(self, window):
        """Depending on class variables menu, playing, and game_over, different prompts
        are displayed, calls info_message and get_coords to do so."""
        if self.prompt=="options":
            window.clear()
            window.addstr(0,0, "Press a/z to i/d dif, r to reveal, b for back.")
            window.chgat(0,0,curses.COLS-4,curses.color_pair(4))
        elif self.prompt=="menu":
            window.clear()
            window.addstr(0,0, "Press r to start the game, o for options, q to quit.")
            window.chgat(0,0,curses.COLS-4,curses.color_pair(4))
        elif self.prompt=="gamescr":
            window.clear()
            window.addstr(0,0,"Enter x and y coordinates: {},{}{}".format(self.fcrds[0],self.fcrds[1], self.fcrds[2]))
            window.chgat(0,0,curses.COLS-4, curses.color_pair(3))
        else:
            window.clear()
            window.addstr("Win = {}. You have {} wins and {} losses.".format(self.win, self.win_counter, self.loss_counter))
            window.chgat(0,0,curses.COLS-4, curses.color_pair(3))

    def menu_input(self, input):
        """Inputs for when in menu"""
        if input == ord('r'):
            self.prompt="gamescr"
            self.make_board()
        if input == ord('o'):
            self.prompt="options"
        if input == ord('q'):
            self.playing=False

    def options_input(self, input):
        """Inputs for when player is in options menu"""
        if input == ord('a'):
            if self.difficulty<10:
                self.difficulty+=1
        if input == ord('z'):
            if self.difficulty>1:
                self.difficulty-=1
        if input == ord('b'):
            self.prompt="menu"
        if input == ord('r'):
            self.revealed=not self.revealed
        if input == 'q':
            self.playing=False

    def playing_input(self, input):
        """Inputs for when player is in gamescr mode"""
        try:
            if input == 10 and self.toggle2:
                self.toggle = True
                self.toggle2 = True
                self.fcrds=[' ',' ',' ']
                return
            input = chr(input)
            if input == 'q':
                self.playing=False
            if input == 'b':
                self.return_menu()
                return
            if self.toggle:
                self.coords[0]=input
                self.fcrds[0]=input
                self.toggle = not self.toggle
            elif self.toggle2:
                self.coords[1]=input
                self.fcrds[1]=input
                self.toggle2 = not self.toggle2
            else:
                self.fcrds=[' ',' ',' ']
                self.coords[2]=input
                # This bit of logic decides if the game ends or not
                if self.parse_coords(self.coords):
                    self.win = False
                    self.update_stats()
                    self.return_menu()
                    return
                if self.mine_brd.rtiles == self.mine_brd.alltiles - self.mine_brd.mtiles:
                    self.win = True
                    self.update_stats()
                    self.return_menu()
                    return
                self.toggle = not self.toggle
                self.toggle2 = not self.toggle2
        except ValueError or AttributeError:
            self.fcrds=[' ',' ',' ']
            self.toggle = True
            self.toggle2 = True

    def return_menu(self):
        self.prompt="menu"
        self.toggle = True
        self.toggle2 = True
        self.coords=[' ',' ',' ']
        self.fcrds=[' ',' ',' ']
        self.first_move = True

    def parse_coords(self, coords):
        board = self.mine_brd
        x = int(coords[0])
        y = int(coords[1])
        if self.first_move:
            board[y][x].selected=True
            self.first_move = False
            # plants mines and counts numbers
            self.make_board()
        if coords[2] == 'f':
            board.flag_cell(y, x)
        else:
            # flip_cell() returns True if the cell is a mine
            if board.flip_cell(y,x):
                 return True
        return False

    def add_brd_str(self, window):
        """Displays string onto board window, usually all cells of the array into a curses window"""
        board = self.mine_brd
        if self.prompt == "menu" or self.prompt == "options":
            window.clear()
            window.addstr("difficulty: "+str(self.difficulty)+"\n")
            window.addstr("wins: "+str(self.win_counter)+"\n")
            window.addstr("losses: "+str(self.loss_counter)+"\n")
            window.addstr("revealed: "+str(self.revealed)+"\n")
        elif self.prompt == "gamescr":
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

    def make_board(self):
        if self.first_move:
            self.mine_brd = Board()
        else:
            self.mine_brd.plant_mines(self.difficulty)
            self.mine_brd.count_surrounding()
        if self.revealed:
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
        """Handles input and refreshes windows"""
        # If in menu input is handled here, windows will resize correctly, if done after they won't
        # Absolutely must handle input only once and quickly
        input = self.stdscr.getch()
        if self.prompt=="options":
            self.options_input(input)
        elif self.prompt=="menu":
            self.menu_input(input)
        elif self.prompt=="gamescr":
            self.playing_input(input)
        else:
            pass

        # Resizes main screen
        y, x = self.stdscr.getmaxyx()
        curses.resize_term(y, x)
        curses.KEY_RESIZE
        self.stdscr.noutrefresh()

        self.title_window()
        self.prompt_window()
        self.board_window()

        # Adds the str to the windows
        self.add_brd_str(self.sub_windows["board"])
        self.prompt_message(self.sub_windows["prompt"])

        # Refreshes all windows
        for i in self.windows:
            self.windows[i].noutrefresh()

        for i in self.sub_windows:
            self.sub_windows[i].noutrefresh()

        curses.doupdate()

    def init_windows(self):
        """Refreshes all windows once without handling input"""
        y, x = self.stdscr.getmaxyx()
        curses.resize_term(y, x)
        curses.KEY_RESIZE
        self.stdscr.noutrefresh()

        self.title_window()
        self.prompt_window()
        self.board_window()

        # Adds the str to the windows
        self.add_brd_str(self.sub_windows["board"])
        self.prompt_message(self.sub_windows["prompt"])

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
    while UI.playing:
        UI.refresh_windows()

    # End of program
    UI.restore_term()
    print ("You had {} wins and {} losses!".format(UI.win_counter, UI.loss_counter))

if __name__ == "__main__":
    """Curses wrapper lets me debug without fucking up terminal windows"""
    wrapper(main)
