"""
Student portion of Zombie Apocalypse mini-project
"""
import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """
    def __init__(self, grid_height, grid_width, obstacle_list = None,
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list:
            self._human_list = list(human_list)
        else:
            self._human_list = []

    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []

    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))

    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)

    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        # replace with an actual generator
        for zombie in self._zombie_list:
            yield zombie

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))

    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)

    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        # replace with an actual generator
        for human in self._human_list:
            yield human

    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        visited = poc_grid.Grid(self._grid_height, self._grid_width)
        distance_field = [[self._grid_height * self._grid_width for dummy_col
            in range(self._grid_width)] for dummy_row
            in range(self._grid_height)]
        boundary = poc_queue.Queue()

        for cell in self._zombie_list if entity_type == ZOMBIE else self._human_list:
            boundary.enqueue(cell)
        for cell in boundary:
            visited.set_full(cell[0], cell[1])
            distance_field[cell[0]][cell[1]] = 0
        for row in range(self._grid_height):
            for col in range(self._grid_width):
                if not self.is_empty(row, col):
                    visited.set_full(row, col)

        while boundary:
            cell = boundary.dequeue()
            neighbors = visited.four_neighbors(cell[0], cell[1])
            for neighbor in neighbors:
                if visited.is_empty(neighbor[0], neighbor[1]):
                    visited.set_full(neighbor[0], neighbor[1])
                    distance_field[neighbor[0]][neighbor[1]] = 1 + distance_field[cell[0]][cell[1]]
                    boundary.enqueue(neighbor)
        return distance_field

    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        full_distance = self._grid_height * self._grid_width
        for human_i in range(len(self._human_list)):
            human = self._human_list[human_i]
            moves = self.eight_neighbors(human[0], human[1])
            max_distance = 0
            max_moves = []
            for move in moves:
                distance = zombie_distance_field[move[0]][move[1]]
                if distance >= max_distance and distance < full_distance:
                    if distance > max_distance:
                        del max_moves[:]
                    max_distance = distance
                    max_moves.append(move)
            self._human_list[human_i] = random.sample(max_moves, 1)[0]

    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        for zombie_i in range(len(self._zombie_list)):
            zombie = self._zombie_list[zombie_i]
            moves = self.four_neighbors(zombie[0], zombie[1])
            min_distance = self._grid_height * self._grid_width
            min_moves = []
            for move in moves:
                distance = human_distance_field[move[0]][move[1]]
                if distance <= min_distance:
                    if distance < min_distance:
                        del min_moves[:]
                    min_distance = distance
                    min_moves.append(move)
            self._zombie_list[zombie_i] = random.sample(min_moves, 1)[0]

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

# poc_zombie_gui.run_gui(Apocalypse(30, 40))
