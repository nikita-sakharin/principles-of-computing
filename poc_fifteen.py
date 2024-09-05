"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""
import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """
    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ''
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += '\n'
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, 'Value ' + str(solved_value) + ' not found'

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == 'l':
                assert zero_col > 0, 'move off grid: ' + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == 'r':
                assert zero_col < self._width - 1, 'move off grid: ' + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == 'u':
                assert zero_row > 0, 'move off grid: ' + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == 'd':
                assert zero_row < self._height - 1, 'move off grid: ' + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, 'invalid direction: ' + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        assert target_row > 1 or target_row == 1 and \
            target_col == self.get_width() - 1, \
            'i <= 1 and (i != 1 or j != n - 1)'

        width = self.get_width()
        if self.get_number(target_row, target_col) != 0:
            return False
        for row in range(target_row, self.get_height()):
            for col in range(0 if row != target_row else target_col + 1, width):
                if self.get_number(row, col) != col + width * row:
                    return False

        return True

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        assert target_col > 0, 'j <= 0'
        assert self.lower_row_invariant(target_row, target_col), \
            'lower_row_invariant(i, j) is False'

        move_string = ''
        zero_row, zero_col = self.current_position(target_row, target_col)
        move_string += self.move_zero_to_position(target_row, target_col,
            zero_row, zero_col)
        row, col = self.prev_position(move_string, zero_row, zero_col)
        move_string += self.position_tile(zero_row, zero_col, (row, col),
            target_row, target_col)
        zero_row, zero_col = self.current_position(0, 0)
        move_string += self.move_zero_to_position(zero_row, zero_col,
            target_row, target_col - 1)

        assert self.lower_row_invariant(target_row, target_col - 1), \
            'lower_row_invariant(i, j - 1) is False'
        return move_string

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row, 0), \
            'lower_row_invariant(i, 0) is False'

        zero_row, zero_col = target_row - 1, 1
        move_string = self.move_zero_to_position(target_row, 0,
            zero_row, zero_col)
        row, col = self.current_position(target_row, 0)

        if (row, col) != (target_row, 0):
            move_string += self.move_zero_to_position(zero_row, zero_col,
                row, col)
            zero_row, zero_col = row, col
            row, col = self.prev_position(move_string, zero_row, zero_col)
            move_string += self.position_tile(zero_row, zero_col, (row, col),
                target_row - 1, 1)

            zero_row, zero_col = self.current_position(0, 0) # TODO
            if zero_row == target_row - 1 and zero_col != 0:
                move_string += 'u'
                self.update_puzzle('u')
            move_string += self.move_zero_to_position(zero_row, zero_col,
                target_row - 1, 0)
            move_string += 'ruldrdlurdluurddlur'
            self.update_puzzle('ruldrdlurdluurddlur')

        move_string += self.move_zero_to_position(target_row - 1, 1,
            target_row - 1, self.get_width() - 1)

        assert self.lower_row_invariant(target_row - 1, self.get_width() - 1), \
            'lower_row_invariant(i - 1, n - 1) is False'
        return move_string

    def move_zero_to_position(self, zero_row, zero_col, row, col):
        """
        Place zero tile at position (row, col)
        Updates puzzle and returns a move string
        """
        assert self.get_number(zero_row, zero_col) == 0, 'number(i, j) != 0'

        move_string = ''
        if row < zero_row:
            move_string += 'u' * (zero_row - row)
        if col < zero_col:
            move_string += 'l' * (zero_col - col)
        elif zero_col < col :
            move_string += 'r' * (col - zero_col)
        if zero_row < row:
            move_string += 'd' * (row - zero_row)
        self.update_puzzle(move_string)

        assert self.get_number(row, col) == 0, 'number(i, j) != 0'
        return move_string

    def position_tile(self, zero_row, zero_col, position,
        target_row, target_col):
        """
        Moves tile from (row, col) to target position using cyclic moves
        Updates puzzle and returns a move string
        """
        assert self.get_number(zero_row, zero_col) == 0, \
            'number(zero_row, zero_col) != 0'

        move_string = ""
        row, col = position
        while (row, col) != (target_row, target_col):
            assert zero_row <= row and row <= target_row, \
                'zero_row > row or row > target_row'
            assert abs(row - zero_row) + abs(col - zero_col) == 1, \
                'abs(row - zero_row) + abs(col - zero_col) != 1'

            if col != target_col:
                diff = target_col - col
                if col > target_col:
                    move_string += ('ulldr' if row > 0 else 'dllur') * abs(diff)
                else: # target_col > col
                    move_string += ('urrdl' if row > 0 else 'drrul') * abs(diff)
                col += diff
                zero_col += diff
            else: # row != target_row
                if col != zero_col:
                    if row > 0:
                        move_string += 'ur' if col > zero_col else 'ul'
                        zero_row -= 1
                    else:
                        move_string += 'dru' if col > zero_col else 'dlu'
                        row += 1
                    if col > zero_col:
                        zero_col += 1
                    else: # zero_col > col
                        zero_col -= 1
                diff = target_row - row
                move_string += ('lddru' if col > 0 else 'rddlu') * diff
                row += diff
                zero_row += diff

        self.update_puzzle(move_string)
        return move_string

    def prev_position(self, move_string, zero_row, zero_col):
        """
        Return previous position of zero title
        """
        if move_string[-1] == 'l':
            return (zero_row, zero_col + 1)
        elif move_string[-1] == 'r':
            return (zero_row, zero_col - 1)
        elif move_string[-1] == 'u':
            return (zero_row + 1, zero_col)
        elif move_string[-1] == 'd':
            return (zero_row - 1, zero_col)

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        width = self.get_width()
        if self.get_number(0, target_col) != 0 or \
            self.get_number(1, target_col) != target_col + width:
            return False
        for row in range(0, self.get_height()):
            for col in range(0 if row > 1 else target_col + 1, width):
                if self.get_number(row, col) != col + width * row:
                    return False

        return True

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        width = self.get_width()
        if self.get_number(1, target_col) != 0:
            return False
        for row in range(0, self.get_height()):
            for col in range(0 if row > 1 else target_col + 1, width):
                if self.get_number(row, col) != col + width * row:
                    return False

        return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        assert target_col > 1, 'j <= 1'
        assert self.row0_invariant(target_col), 'row0_invariant(j) is False'

        zero_row, zero_col = 1, target_col - 1
        move_string = self.move_zero_to_position(0, target_col,
            zero_row, zero_col)
        row, col = self.current_position(0, target_col)

        if (row, col) != (0, target_col):
            move_string += self.move_zero_to_position(zero_row, zero_col,
                row, col)
            zero_row, zero_col = row, col
            row, col = self.prev_position(move_string, zero_row, zero_col)
            move_string += self.position_tile(zero_row, zero_col, (row, col),
                1, target_col - 1)

            zero_row, zero_col = self.current_position(0, 0) # TODO
            move_string += self.move_zero_to_position(zero_row, zero_col,
                1, target_col - 2)
            move_string += 'urdlurrdluldrruld'
            self.update_puzzle('urdlurrdluldrruld')

        assert self.row1_invariant(target_col - 1), \
            'row1_invariant(j - 1) is False'
        return move_string

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        assert target_col > 1, 'j <= 1'
        assert self.row1_invariant(target_col), 'row1_invariant(j) is False'

        move_string = ''
        zero_row, zero_col = self.current_position(1, target_col)
        move_string += self.move_zero_to_position(1, target_col,
            zero_row, zero_col)
        row, col = self.prev_position(move_string, zero_row, zero_col)
        move_string += self.position_tile(zero_row, zero_col, (row, col),
            1, target_col)
        zero_row, zero_col = self.current_position(0, 0)
        move_string += self.move_zero_to_position(zero_row, zero_col,
            0, target_col)

        assert self.row0_invariant(target_col), 'row0_invariant(j) is False'
        return move_string

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        move_string = self.move_zero_to_position(zero_row, zero_col, 0, 0)
        width = self.get_width()
        for dummy_i in range(3):
            if self.get_number(0, 0) == 0 and self.get_number(0, 1) == 1 and \
                self.get_number(1, 0) == width and \
                self.get_number(1, 1) == width + 1:
                return move_string
            move_string += 'rdlu'
            self.update_puzzle('rdlu')

        assert False, 'permutation is odd'

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        move_string = self.move_zero_to_position(zero_row, zero_col,
            self.get_height() - 1, self.get_width() - 1)
        for row in range(self.get_height() - 1, 1, -1):
            for col in range(self.get_width() - 1, -1, -1):
                if col != 0:
                    move_string += self.solve_interior_tile(row, col)
                else:
                    move_string += self.solve_col0_tile(row)
        for col in range(self.get_width() - 1, 1, -1):
            move_string += self.solve_row1_tile(col)
            move_string += self.solve_row0_tile(col)

        move_string += self.solve_2x2()
        return move_string

# Start interactive simulation
poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))
