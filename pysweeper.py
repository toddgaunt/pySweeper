#! /usr/bin/python3
# author: Todd Gaunt
# apache 2.0
# minesweeper game

import random

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
        self.mined_tiles = mined_tiles
        self.revealed_tiles = revealed_tiles
        self.flagged_tiles = flagged_tiles
        for y in range(self.y_length):
            self.append([])
            for x in range(self.x_length):
                self[y].append(Cell())

    def print_brd(self):
        """Concatenates the board to a string, the returns the value."""
        brdstr = ""
        count = self.y_length - 1
        for y in range(self.y_length):
            brdstr += str(count) + " - "
            for x in range(self.x_length):
                if self[count][x].revealed == True:
                    brdstr += str(self[count][x].tile) + " "
                else:
                    brdstr += "# "
            count -= 1
            brdstr += "\n"
        count = 0
        brdstr += "    "
        brdstr += "| " * self.x_length + "\n"
        brdstr += "    "
        for i in range(self.x_length):
            brdstr += str(count) + " "
            count += 1
        brdstr += "\n"
        return brdstr

    def plant_mines(self):
        """Plants exactly the amount of mines according to algorithm"""
        count = (self.y_length * self.x_length / ((self.y_length + self.x_length) / 2))
        while count > 0:
            y = random.randint(0, self.y_length -1)
            x = random.randint(0, self.x_length -1)
            if self[y][x].mine or self[y][x].selected:
                continue
            else:
                self[y][x].tile = "X"# mine=True
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

    def mined_tiles_count():
        """Counts up all mines"""
        tmp = 0
        for y in range(self.y_length):
            for x in range(self.x_length):
                if self[y][x].mine():
                    tmp += 1
        self.mined_tiles = tmp
        return tmp

    def revealed_tiles_count():
        """Counts up all tiles that have revealed=True"""
        tmp = 0
        for y in range(self.y_length):
            for x in range(self.x_length):
                if not self[y][x].mine():
                    tmp += 1
        self.revealed_tiles = tmp
        return tmp

    def flagged_tiles_count():
        """Counts up all tiles that have revealed=True"""
        tmp = 0
        for y in range(self.y_length):
            for x in range(self.x_length):
                if not self[y][x].mine():
                    tmp += 1
        self.flagged_tiles = tmp
        return tmp

def main():
    """Main driver function, prints to the console"""
    mine_brd = Board()
    print(mine_brd.print_brd())
    coords = get_coords()
    mine_brd.flip_cell(coords[0], coords[1])
    mine_brd.plant_mines()
    mine_brd.count_surrounding()
    game_over = False
    win = False
    # Main loop starts after 1 turn.
    while game_over == False:
        print(mine_brd.print_brd())
        coords = get_coords()
        game_over =  mine_brd.flip_cell(coords[0], coords[1])
        if mine_brd.y_length * mine_brd.x_length - mine_brd.mined_tiles == mine_brd.revealed_tiles:
            game_over = True
            win = True
    mine_brd.print_brd()
    if win == True:
        print ("You win!")
    else:
        print ("You lose...")

def get_coords():
    """Gets coordinate input from the player"""
    print("Please enter x-coordinate")
    x = input()
    print("Please enter y-coordinate")
    y = input()
    coords = [y,x]
    return coords

if __name__ == "__main__":
    main()
