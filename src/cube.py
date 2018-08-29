import random

class Corner:
    def __init__(self, colors : str):
        self.colors = [color for color in colors]
        # e.g. self.colors = [F", "L", "U"]
        # the first element is the colour that is either on top or on the bottom
        # the second is the first sticker clockwise from the first.

    def rotate_clockwise(self):
        self.colors.insert(0, self.colors[-1])
        del self.colors[-1]

class Edge:
    def __init__(self, colors: str):
        self.colors = [color for color in colors]
        # e.g. self.colors = ["R", "F"]
        # the first element is the colour that is on U or D, or on F or D if it is in the E layer

    def flip(self):
        self.colors.reverse()

# Corrects the name of a given corner so that it respects the convention that the colours on
# that corner piece are listed in clockwise order
# @param id: The name of a corner (e.g. UFR) which may or may not list the letters in the correct order
def parse_corner_id(id):
    # determine if it is a U/D corner and identify the other faces
    faces_clockwise = "RFLB"
    UlayerCorner = "U" in id
    first_letter = "U" if UlayerCorner else "D"
    otherfaces = "".join([letter for letter in id if letter != first_letter])

    # rearrange so that the colours are listed in clockwise order
    correct_order = faces_clockwise if UlayerCorner else faces_clockwise[::-1]
    if correct_order[(correct_order.index(otherfaces[0]) + 1) % len(correct_order)] == otherfaces[1]:
        return first_letter + otherfaces
    else:
        return first_letter + otherfaces[::-1]

# Corrects the name of a given edge so that it respects the convention that id[0] in "UD" or id[1] in "RL"
# @param id: The name of a edge (e.g. BR) which may or may not list the letters in the correct order
def parse_edge_id(id):
    if id[0] in "UD" or id[1] in "RL":
        return id
    else:
        return id[::-1]

class Cube:

    corner_locations = ["ULB", "UBR", "URF", "UFL", "DBL", "DRB", "DFR", "DLF"]
    edge_locations = ["UB", "UR", "UF", "UL", "DB", "DR", "DF", "DL", "FL", "FR", "BL", "BR"]

    # create a solved cube
    def __init__(self):
        # dictionary with the location as the key and the colours as the value
        self.corners = {}
        for corner in Cube.corner_locations:
            self.corners[corner] = Corner(corner)

        self.edges = {}
        for edge in Cube.edge_locations:
            self.edges[edge] = Edge(edge)

    # returns a string that reads the stickers as required by the kociemba library
    def __str__(self):
        return\
            self.corners["ULB"].colors[0] +\
            self.edges["UB"].colors[0] +\
            self.corners["UBR"].colors[0] +\
            self.edges["UL"].colors[0] +\
            "U" +\
            self.edges["UR"].colors[0] +\
            self.corners["UFL"].colors[0] +\
            self.edges["UF"].colors[0] +\
            self.corners["URF"].colors[0] +\
            \
            self.corners["URF"].colors[1] +\
            self.edges["UR"].colors[1] +\
            self.corners["UBR"].colors[2] +\
            self.edges["FR"].colors[1] +\
            "R" +\
            self.edges["BR"].colors[1] +\
            self.corners["DFR"].colors[2] +\
            self.edges["DR"].colors[1] +\
            self.corners["DRB"].colors[1] +\
            \
            self.corners["UFL"].colors[1] +\
            self.edges["UF"].colors[1] +\
            self.corners["URF"].colors[2] +\
            self.edges["FL"].colors[0] +\
            "F" +\
            self.edges["FR"].colors[0] +\
            self.corners["DLF"].colors[2] +\
            self.edges["DF"].colors[1] +\
            self.corners["DFR"].colors[1] +\
            \
            self.corners["DLF"].colors[0] +\
            self.edges["DF"].colors[0] +\
            self.corners["DFR"].colors[0] +\
            self.edges["DL"].colors[0] +\
            "D" +\
            self.edges["DR"].colors[0] +\
            self.corners["DBL"].colors[0] +\
            self.edges["DB"].colors[0] +\
            self.corners["DRB"].colors[0] +\
            \
            self.corners["ULB"].colors[1] +\
            self.edges["UL"].colors[1] +\
            self.corners["UFL"].colors[2] +\
            self.edges["BL"].colors[1] +\
            "L" +\
            self.edges["FL"].colors[1] +\
            self.corners["DBL"].colors[2] +\
            self.edges["DL"].colors[1] +\
            self.corners["DLF"].colors[1] +\
            \
            self.corners["UBR"].colors[1] +\
            self.edges["UB"].colors[1] +\
            self.corners["ULB"].colors[2] +\
            self.edges["BR"].colors[0] +\
            "B" +\
            self.edges["BL"].colors[0] +\
            self.corners["DRB"].colors[2] +\
            self.edges["DB"].colors[1] +\
            self.corners["DBL"].colors[1]

    # twist all the corners of this cube randomly while keeping the cube solvable
    # @param corners:   the corners that should be scrambled
    def random_corner_orientation(self, corners = corner_locations):
        # twist each corner clockwise, counterclockwise, or not at all
        total_clockwise_turns = 0
        for i in range(len(corners) - 1):
            num_clockwise_turns = int(3*random.random()) # [0..2]
            for k in range(num_clockwise_turns):
                self.corners[corners[i]].rotate_clockwise()
            total_clockwise_turns = (total_clockwise_turns + num_clockwise_turns) % 3

        # avoid CO parity by twisting the last corner correctly
        for i in range((3 - total_clockwise_turns) % 3):
            self.corners[corners[-1]].rotate_clockwise()

    # flip all the edges of this cube randomly while keeping the cube solvable
    # @param edges:   the edges that should be scrambled
    def random_edge_orientation(self, edges = edge_locations):
        # Determine for each edge if it should be flipped
        even_number_flips = True
        for i in range(len(edges) - 1):
            if random.random() < 0.5:
                self.edges[edges[i]].flip()
                even_number_flips = not even_number_flips

        # avoid EO parity by flipping the last edge correctly
        if not even_number_flips:
            self.edges[edges[-1]].flip()

    # @param corners: the corners that should be scrambled
    # @param edges:   the edges that should be scrambled
    def random_permutation(self, corners = corner_locations, edges = edge_locations):

        def swap_corners(i, j):
            tmp = self.corners[corners[i]]
            self.corners[corners[i]] = self.corners[corners[j]]
            self.corners[corners[j]] = tmp

        def swap_edges(i, j):
            tmp = self.edges[edges[i]]
            self.edges[edges[i]] = self.edges[edges[j]]
            self.edges[edges[j]] = tmp

        even_num_swaps = True
        # Fischer-Yates shuffle the corners
        for i in range(len(corners) - 1):
            j = int(random.uniform(i, len(corners)))
            if i != j:
                swap_corners(i, j)
                even_num_swaps = not even_num_swaps

        # Fischer-Yates shuffle the edges
        for i in range(len(edges) - 1):
            j = int(random.uniform(i, len(edges)))
            if i != j:
                swap_edges(i, j)
                even_num_swaps = not even_num_swaps

        if not even_num_swaps:
            if len(corners) == 0:
                swap_edges(0, 1)
            elif len(edges) == 0 or random.random() < 0.5:
                swap_corners(0, 1)
            else:
                swap_edges(0, 1)

    # flip exacly n edges of this cube randomly
    # @param edges:   the edges that should be scrambled
    def flip_n_edges(self, edge_locations, n):
        if n % 2 != 0:
            raise ValueError("Cannot flip an odd number of edges.")
        flipped_edges = random.sample(edge_locations, n)
        for edge in flipped_edges:
            self.edges[edge].flip()
