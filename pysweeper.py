#! /usr/bin/python3
# author: Todd Gaunt
# apache 2.0
# minesweeper game

import random

class Cell(object):
    """Is a single cell of the minesweeper board"""
    def __init__(self, mine=False, revealed=False, flagged=False, tile=0):
        self.mine = mine # Whether or not there is a mine
        self.revealed = revealed # Whether or not the player can see the tile
        self.flagged = flagged # Whether or not the player marked the tile
        self.tile = tile # The character used to represent the tile

    def show(self):
        self.revealed = True

    def flag(self):
        """toggles flags on a tile"""
        self.flagged = not self.flagged

    def get_tile(self):
        """returns a string if the tile is an X, an int if the tile is a number"""
        return self.tile

    def set_tile(self, mine=False, tile=0):
        self.tile = tile
        self.mine = mine

    def increment_tile(self):
        if self.tile != "X":
            self.tile += 1

class Board(list):
    """This Board object contains Cell objects within itself to represent the minesweeper game board"""
    def __init__(self, x_length=10, y_length=10, mine_count=0, revealed_tiles=0):
        self.x_length = x_length # Length of board's x-axis
        self.y_length = y_length # Length of board's y-axis
        self.mine_count = mine_count # Amount of mines on the board
        self.revealed_tiles = revealed_tiles
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
                current_cell = self[count][x]
                if current_cell.revealed == True:
                    brdstr += str(current_cell.get_tile()) + " "
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
            cur_cell = self[y][x]
            if cur_cell.get_tile() == "X" or cur_cell.revealed:
                continue
            else:
                cur_cell.set_tile(True, "X")
                self.mine_count += 1
                count -= 1

    def count_surrounding(self):
        """Uses a coordinate list to check surrounding tiles of mines and increments them if there is no mine"""
        coordinates = [[-1, -1], [-1, 0], [-1, 1],
                       [0 , -1],          [0 , 1],
                       [1 , -1], [1 , 0], [1 , 1]]
        for y in range(self.y_length):
            for x in range(self.x_length):
                if self[y][x].get_tile() == "X":
                    for i in range(len(coordinates)):
                        y_offset = y+coordinates[i][0]
                        x_offset = x+coordinates[i][1]
                        if y_offset < 0 or y_offset >= self.y_length or x_offset >= self.x_length or x_offset < 0:
                            continue
                        self[y_offset][x_offset].increment_tile()

    def get_cell(self, y=0, x=0):
        return self[y][x]

    def flip_cell(self, y, x):
        """Reveals the tile according to x,y coordinates. If the tile is a  mine returns True, else False."""
        coordinates = [          [-1, 0],
                       [0 , -1],          [0 , 1],
                                 [1 , 0]]
        y = int(y)
        x = int(x)
        if self[y][x].revealed:
            return False

        # Reveals current cell
        self[y][x].show()
        self.revealed_tiles += 1

        if self[y][x].get_tile() == "X":
            return True

        if self[y][x].get_tile() == 0:
            for i in range(len(coordinates)):
                y_offset = y+coordinates[i][0]
                x_offset = x+coordinates[i][1]
                if y_offset < 0 or y_offset >= self.y_length or x_offset >= self.x_length or x_offset < 0:
                    continue
                self.flip_cell(y_offset, x_offset)

    @property
    def remaining_mines():
        pass

    @property
    def revealed_tile_count():
        pass

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
        if mine_brd.y_length * mine_brd.x_length - mine_brd.mine_count == mine_brd.revealed_tiles:
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
