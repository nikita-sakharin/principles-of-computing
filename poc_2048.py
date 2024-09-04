"""
Clone of 2048 game.
"""
import random
import poc_2048_gui

UP, DOWN, LEFT, RIGHT = 1, 2, 3, 4

OFFSETS = {
    UP:    (1,  0),
    DOWN:  (-1, 0),
    LEFT:  (0,  1),
    RIGHT: (0, -1)
}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    result = [0] * len(line)
    idx, last_merge = 0, 0
    for value in line:
        if value == 0:
            continue
        result[idx] = value
        if idx > last_merge and result[idx - 1] == result[idx]:
            result[idx - 1] *= 2
            result[idx] = 0
            last_merge = idx
        else:
            idx += 1
    return result

class TwentyFortyEight:
    """
    Class to run the game logic.
    """
    def __init__(self, grid_height, grid_width):
        self._height = grid_height
        self._width = grid_width
        self._initial = {
            UP:    [(0,                idx) for idx in range(self._width)],
            DOWN:  [(self._height - 1, idx) for idx in range(self._width)],
            LEFT:  [(idx,                0) for idx in range(self._height)],
            RIGHT: [(idx,  self._width - 1) for idx in range(self._height)],
        }
        self.reset()

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._grid = [[0] * self._width for _ in range(self._height)]
        for _ in range(2):
            self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        return str(self._grid)

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        delta = OFFSETS[direction]
        length = self._height if direction in { UP, DOWN } else self._width
        temporary = [0] * length
        changed = False
        for pos in self._initial[direction]:
            for idx in range(length):
                temporary[idx] = \
                    self._grid[pos[0] + delta[0] * idx][pos[1] + delta[1] * idx]
            temporary = merge(temporary)
            for idx in range(length):
                prev = self._grid[pos[0] + delta[0] * idx][pos[1] + delta[1] * idx]
                changed |= prev != temporary[idx]
                self._grid[pos[0] + delta[0] * idx][pos[1] + delta[1] * idx] = \
                    temporary[idx]
        if changed:
            self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        empty_count = 0
        for row in range(self._height):
            empty_count += self._grid[row].count(0)
        if empty_count == 0:
            return
        square_index = random.randint(0, empty_count - 1)
        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] != 0:
                    continue
                if square_index == 0:
                    self._grid[row][col] = 2 if random.randint(0, 9) != 9 else 4
                    return
                square_index -= 1

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col]

poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
