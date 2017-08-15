class Corner:
    def __init__(self, colors : str):
        self.colors = [color for color in colors]
        # e.g. self.colors = [F", "L", "U"]
        # the first element is the colour that is either on top or on the bottom
        # the second is the first sticker clockwise from the first.

    def rotateClockwise(self):
        self.colors.insert(0, self.colors[-1])
        del self.colors[-1]

    def rotateCounterClockwise(self):
        self.rotateCW()
        self.rotateCW()

class Edge:
    def __init__(self, colors: str):
        self.colors = [color for color in colors]
        # e.g. self.colors = ["R", "F"]
        # the first element is the colour that is on U or D, or on F or D if it is in the E layer

    def flip(self):
        self.colors.reverse()

class Cube:
    # create a solved cube
    def __init__(self):
        # dictionary with the location as the key and the colours as the value
        self.corners = {}
        for corner in ["ULB", "UBR", "URF", "UFL", "DBL", "DRB", "DFR", "DLF"]:
            self.corners[corner] = Corner(corner)

        self.edges = {}
        for edge in ["UB", "UR", "UF", "UL", "DB", "DR", "DF", "DL", "FL", "FR", "BL", "BR"]:
            self.edges[edge] = Edge(edge)
