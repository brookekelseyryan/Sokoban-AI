import numpy as np

# String constants for each component of the Sokoban puzzle
WALL = "#"
AGENT = "@"
GOAL = "."
BOX = "$"

# Constants for the line numbers in the input and what data they represent
BOARD_DIMENSIONS_LINE = 0
WALL_SQUARES_LINE = 1
BOXES_LINE = 2
GOALS_LINE = 3
AGENT_LINE = 4


#
# Processes the input file and initializes the corresponding components of the Sokoban board.
#
class Sokoban:

    box_locations = []
    agent_location = None

    # Initialization of the board requires the path to the sokoban__.txt file
    def __init__(self, path_to_file):

        # Each line of the file is an element in the list
        file_contents = open(path_to_file).readlines()
        lines = list(map(lambda x: x.replace('\n', '').split(' '), file_contents))

        # List is converted to numpy array of integers for ease of data manipulation
        data = np.array([np.array(x, dtype=np.int8) for x in lines], dtype=object)

        # Initialize the 2D string list used to represent the board
        self.dimensions(data[BOARD_DIMENSIONS_LINE])

        # Get the constants from the file
        self.n_wall_squares = data[WALL_SQUARES_LINE][0]
        self.n_boxes = data[BOXES_LINE][0]
        self.n_goals = data[GOALS_LINE][0]

        # Decrement each element by one once constants have been extracted for proper array indexing
        data = data - 1

        # Get the coordinates of the walls, boxes, goals, and agent and set appropriately in the 2D string list
        self.wall_squares(data[WALL_SQUARES_LINE][1:])
        self.boxes(data[BOXES_LINE][1:])
        self.goals(data[GOALS_LINE][1:])
        self.agent(data[AGENT_LINE])

    # Prints the board in the same format as Kask
    def print(self):
        for x in self.board:
            line = ''
            for y in x:
                line += y
            print(line)

    # Init the board based on the dimensions (x,y)
    def dimensions(self, line):
        self.height = line[1]
        self.length = line[0]

        # Python 2D List of Strings
        self.board = [[' ' for x in range(self.length)] for y in range(self.height)]

    # Number of wall squares is the first number on the second line
    def wall_squares(self, line):
        for i in range(0, len(line), 2):
            row = line[i]
            col = line[i + 1]
            self.board[row][col] = WALL

    def goals(self, line):
        for i in range(0, len(line), 2):
            row = line[i]
            col = line[i + 1]
            self.board[row][col] = GOAL

    def boxes(self, line):
        for i in range(0, len(line), 2):
            row = line[i]
            col = line[i + 1]
            self.board[row][col] = BOX
            self.box_locations += [(row,col)]

    # Agent coordinates (x,y) are the first and second elements on the fifth line
    def agent(self, line):
        row = line[0]
        col = line[1]
        self.board[row][col] = AGENT
        self.agent_location = (row,col)

#
# Box object contains location coordinates and available moves
#
class Box:
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.moves = []

#
# Agent contains location coordinates
#
class Agent:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.coordinates = (row, col)
        self.moves = []