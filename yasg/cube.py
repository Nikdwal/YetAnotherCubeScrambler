import random

class Corner:
    def __init__(self, colors : str):
        self.colors = [color for color in colors]
        self.oriented_color_order = colors
        # e.g. self.colors = [F", "L", "U"]
        # the first element is the colour that is either on top or on the bottom
        # the second is the first sticker clockwise from the first.

    def rotate_clockwise(self, num_times = 1):
        for _ in range(num_times):
            self.colors.insert(0, self.colors[-1])
            del self.colors[-1]

    def is_oriented(self):
        return self.colors[0] == self.oriented_color_order[0]

class Edge:
    def __init__(self, colors: str):
        self.colors = [color for color in colors]
        self.oriented_color_order = colors
        # e.g. self.colors = ["R", "F"]
        # the first element is the colour that is on U or D, or on F or D if it is in the E layer

    def flip(self):
        self.colors.reverse()

    def is_oriented(self):
        if self.colors[0] in ["U", "D"]:
            return True
        return self.colors[1] not in ["U", "D"] and self.colors[0] in ["F", "B"]

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

    _clockwise_corner_order = {
        "U" : ["URF", "UFL", "ULB", "UBR"],
        "D" : ["DLF", "DFR", "DRB", "DBL"],
        "R" : ["URF", "UBR", "DRB", "DFR"],
        "L" : ["ULB", "UFL", "DLF", "DBL"],
        "F" : ["UFL", "URF", "DFR", "DLF"],
        "B" : ["UBR", "ULB", "DBL", "DRB"]
    }
    _clockwise_edge_order = {
        "U" : ["UB", "UR", "UF", "UL"],
        "D" : ["DF", "DR", "DB", "DL"],
        "R" : ["UR", "BR", "DR", "FR"],
        "L" : ["UL", "FL", "DL", "BL"],
        "F" : ["UF", "FR", "DF", "FL"],
        "B" : ["UB", "BL", "DB", "BR"]
    }

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
            self.corners[corners[i]].rotate_clockwise(num_clockwise_turns)
            total_clockwise_turns = (total_clockwise_turns + num_clockwise_turns) % 3

        # avoid CO parity by twisting the last corner correctly
        if total_clockwise_turns % 3 != 0:
            self.corners[corners[-1]].rotate_clockwise((- total_clockwise_turns) % 3)

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

    def _swap_corners(self, location1, location2):
        tmp = self.corners[location1]
        self.corners[location1] = self.corners[location2]
        self.corners[location2] = tmp
        
    def _swap_edges(self, location1, location2):
        tmp = self.edges[location1]
        self.edges[location1] = self.edges[location2]
        self.edges[location2] = tmp

    # @param corners: the corners that should be scrambled
    # @param edges:   the edges that should be scrambled
    def random_permutation(self, corners = corner_locations, edges = edge_locations):

        even_num_swaps = True
        # Fischer-Yates shuffle the corners
        for i in range(len(corners) - 1):
            j = int(random.uniform(i, len(corners)))
            if i != j:
                self._swap_corners(corners[i], corners[j])
                even_num_swaps = not even_num_swaps

        # Fischer-Yates shuffle the edges
        for i in range(len(edges) - 1):
            j = int(random.uniform(i, len(edges)))
            if i != j:
                self._swap_edges(edges[i], edges[j])
                even_num_swaps = not even_num_swaps

        if not even_num_swaps:
            if len(corners) == 0:
                self._swap_edges(edges[0], edges[1])
            elif len(edges) == 0 or random.random() < 0.5:
                self._swap_corners(corners[0], corners[1])
            else:
                self._swap_edges(edges[0], edges[1])

    # flip exacly n edges of this cube randomly
    # @param edges:   the edges that should be scrambled
    def flip_n_edges(self, edge_locations, n):
        n = int(n)
        if n % 2 != 0:
            raise ValueError("Cannot flip an odd number of edges.")
        flipped_edges = random.sample(edge_locations, n)
        for edge in flipped_edges:
            self.edges[edge].flip()

    # Do a U turn
    def Umove(self, num_turns=1):
        adj_faces_cw = "FLBR"
        U_corners = sorted([corner for corner in Cube.corner_locations if "U" in corner], key=lambda corner : adj_faces_cw.index(corner[1]))
        U_edges   = sorted([edge for edge in Cube.edge_locations if "U" in edge], key=lambda edge : adj_faces_cw.index(edge[1]))
        prev_corners = [self.corners[c] for c in U_corners]
        prev_edges   = [self.edges[e] for e in U_edges]
        for i in range(4):
            self.corners[U_corners[i]] = prev_corners[i - num_turns]
            self.edges[U_edges[i]] = prev_edges[i - num_turns]

    def _cycle_pieces_on_face(self, corners_cw, edges_cw, num_turns=1):
        prev_corners = [self.corners[c] for c in corners_cw]
        prev_edges = [self.edges[e] for e in edges_cw]
        for i in range(4):
            self.corners[corners_cw[i]] = prev_corners[i - num_turns]
            self.edges[edges_cw[i]] = prev_edges[i - num_turns]

    def _twist_corners_alternating(self, corners_cw):
        # assume that a single turn on a solved cube twists the first corner location by two clockwise turns
        i = 2
        for corner in corners_cw:
            self.corners[corner].rotate_clockwise(i)
            i = (2*i) % 3 # pattern: 2 1 2 1 2 ...

    def move_layer(self, layer, num_turns = 1):
        corners = Cube._clockwise_corner_order[layer]
        edges   = Cube._clockwise_edge_order[layer]
        self._cycle_pieces_on_face(corners, edges, num_turns)
        if layer in "RFLB":
            if num_turns % 2 == 1:
                self._twist_corners_alternating(corners)
            if layer in "FB" and num_turns % 2 == 1:
                for edge in edges:
                    self.edges[edge].flip()


    def randomAUF(self):
        self.Umove(int(random.uniform(0,4)))

    def apply_algorithm(self, alg : str):
        alg = alg.replace(" ", "")
        i = 0
        while i < len(alg):
            start_next_move = len(alg)
            for j in range(i+1, len(alg)):
                if alg[j].isalpha():
                    start_next_move = j
                    break
            if start_next_move <= i:
                start_next_move = len(alg)
            move = alg[i:start_next_move]
            if len(move) == 1:
                self.move_layer(move)
            elif move[-1] == "2":
                self.move_layer(move[0], 2)
            elif move[-1] == "\'":
                self.move_layer(move[0], 3)
            else:
                raise ValueError("Invalid algorithm: " + alg)
            i = start_next_move

    def orient_U_corners(self):
        self.orient_corners(self._clockwise_corner_order["U"], ["DFR"])

    def corner_is_solved(self, location):
        return self.corners[location].oriented_color_order == location

    def edge_is_solved(self, location):
        return self.edges[location].oriented_color_order == location

    def arrange(self, corners, edges, buffer_corners, buffer_edges):
        # shuffle the pieces randomly so that each permutation is equally likely.
        self.random_permutation(corners + buffer_corners, edges + buffer_edges)

        arranged_corner_locations = set(corners)
        arranged_edge_locations   = set(edges)
        deranged_corner_locations = set(buffer_corners)
        deranged_edge_locations   = set(buffer_edges)

        # make an inverse map of self.corners and self.edges, i.e.
        # store the current location of the piece for each piece
        corner_location_map = {}
        edge_location_map = {}
        def update_corner_map(locations):
            for location in locations:
                corner_location_map[self.corners[location].oriented_color_order] = location
        def update_edge_map(locations):
            for location in locations:
                edge_location_map[self.edges[location].oriented_color_order] = location
        update_corner_map(Cube.corner_locations)
        update_edge_map(Cube.edge_locations)

        # shuffle these pieces so that each permutation is equally likely

        # Iterate through the corner/edge locations you want to permute correcly and swap the
        # piece that is in this spot with the piece that belongs there
        even_number_of_swaps = True
        for location in corners:
            if self.corner_is_solved(location):
                continue

            spot_of_piece_that_belongs_here = corner_location_map[location]
            even_number_of_swaps = not even_number_of_swaps
            self._swap_corners(location, spot_of_piece_that_belongs_here)
            update_corner_map([location, spot_of_piece_that_belongs_here])

            # We have disturbed a corner that wasn't specified by the user (although it was necessary)
            # Remember this for the parity check at the end
            if spot_of_piece_that_belongs_here not in arranged_corner_locations:
                deranged_corner_locations.add(spot_of_piece_that_belongs_here)

        # God copying this over is ugly.
        for location in edges:
            # check if already solved
            if self.edge_is_solved(location):
                continue

            spot_of_piece_that_belongs_here = edge_location_map[location]
            even_number_of_swaps = not even_number_of_swaps
            self._swap_edges(location, spot_of_piece_that_belongs_here)
            update_edge_map([location, spot_of_piece_that_belongs_here])

            # We have disturbed an edge that wasn't specified by the user (although it was necessary)
            # Remember this for the parity check at the end
            if spot_of_piece_that_belongs_here not in arranged_edge_locations:
                deranged_edge_locations.add(spot_of_piece_that_belongs_here)

        # All the specified pieces should be solved now. We still have to check for parity.
        if not even_number_of_swaps:
            # Swap two of the deranged pieces if possible
            swap_corners = True
            if len(deranged_corner_locations) < 2:
                if len(deranged_edge_locations) < 2:
                    # There aren't enough deranged pieces. We must select some random victims.
                    untouched_pieces = set(Cube.corner_locations).difference(arranged_corner_locations.union(deranged_corner_locations))
                    deranged_corner_locations.update(random.sample(untouched_pieces, 2 - len(deranged_corner_locations)))
                else:
                    swap_corners = False # Swap the edges instead
                    i, j = tuple(random.sample(deranged_edge_locations, 2))
                    self._swap_edges(i, j)
            if swap_corners:
                i, j = tuple(random.sample(deranged_corner_locations, 2))
                self._swap_corners(i, j)

    def derange(self, corners, edges, buffer_corners, buffer_edges):
        # shuffle the pieces randomly so that each permutation is equally likely.
        self.random_permutation(corners + buffer_corners, edges + buffer_edges)
        even_number_of_swaps = True

        # functions that determine if swapping two pieces would result in either of them being solved.
        can_swap_corners = lambda c1, c2 : c1 != self.corners[c2].oriented_color_order and c2 != self.corners[c1].oriented_color_order
        can_swap_edges   = lambda e1, e2 : e1 != self.edges[e2].oriented_color_order   and e2 != self.edges[e1].oriented_color_order

        # Swap pieces[i] with another piece
        # pieces = corners/edges (the parameter from the user)
        # i = the index within "pieces"
        # self_pieces = self.corners or self.edges
        # return: true iff you swapped a piece
        def derange_piece(pieces, i, swap_pieces, can_swap_pieces, buffer):
            # Iterate through the pieces that have to be deranged to find a swap.
            # If we can't find a piece to swap with, we continue iterating through the buffer.
            for j in range(1, len(pieces) + len(buffer)):
                if j < len(pieces):
                    other_location = pieces[(i + j) % len(pieces)]
                else:
                    other_location = buffer[j - len(pieces)]
                if can_swap_pieces(pieces[i], other_location):
                    swap_pieces(pieces[i], other_location)
                    return True # swapped a piece
            # If this piece is solved and you can't swap this with any piece with any other piece,
            # you can't derange all the given pieces while leaving the other ones untouched,
            # even using the buffer
            return False

        # Some pieces might happen to be solved, even after permuting them randomly.
        # Try to swap them with another piece.
        for i in range(len(corners)):
            if self.corner_is_solved(corners[i]):
                piece_was_swapped = derange_piece(corners, i, self._swap_corners, can_swap_corners, buffer_corners)
                if piece_was_swapped:
                    even_number_of_swaps = not even_number_of_swaps

        for i in range(len(edges)):
            if self.edge_is_solved(edges[i]):
                piece_was_swapped = derange_piece(edges, i, self._swap_edges, can_swap_edges, buffer_edges)
                if piece_was_swapped:
                    even_number_of_swaps = not even_number_of_swaps

        # Try to make up for an odd number of swaps. There are many methods that may succeed.
        # If a method failed, go to a less preferable method.
        if not even_number_of_swaps:
            # See if you can swap any corners (not necessarily solved ones)
            for i in range(len(corners)):
                piece_was_swapped = derange_piece(corners, i, self._swap_corners, can_swap_corners, buffer_corners)
                if piece_was_swapped:
                    return
            # That failed. Maybe you could try edges
            for i in range(len(edges)):
                piece_was_swapped = derange_piece(edges, i, self._swap_edges, can_swap_edges, buffer_edges)
                if piece_was_swapped:
                    return
            # That failed as well. Just swap two buffer pieces randomly.
            if len(buffer_corners) >= 2:
                self._swap_corners(buffer_corners[0], buffer_corners[1])
            elif len(buffer_edges) >= 2:
                self._swap_edges(edges[0], edges[1])
            # Even that failed. It turns out we can't derange the pieces with an even number of swaps.
            # Just select two victims and swap those.
            elif len(corners) >= 2:
                self._swap_corners(corners[0], corners[1])
            else:
                self._swap_edges(edges[0], edges[1])

    def _flip_edge_if(self, edges, buffer, condition):
        # Make every orientation equally likely
        self.random_edge_orientation(edges + buffer)

        num_flips = 0
        for edge_location in edges:
            edge = self.edges[edge_location]
            if condition(edge):
                num_flips +=1
                edge.flip()
        if num_flips % 2 != 0:
            victim = random.choice(buffer if buffer else edges)
            self.edges[victim].flip()

    def orient_edges(self, edges, buffer):
        self._flip_edge_if(edges, buffer, lambda e : not e.is_oriented())

    def disorient_edges(self, edges, buffer):
        self._flip_edge_if(edges, buffer, lambda e : e.is_oriented())

    def orient_corners(self, corners, buffer):
        # Make every orientation equally likely
        self.random_corner_orientation(corners + buffer)

        num_twists = 0
        for corner_location in corners:
            corner = self.corners[corner_location]
            n = (- corner.colors.index(corner.oriented_color_order[0])) % 3
            corner.rotate_clockwise(n)
            num_twists += n
        if num_twists % 3 != 0:
            victim = random.choice(buffer if buffer else corners)
            self.corners[victim].rotate_clockwise((- num_twists) % 3)

    def disorient_corners(self, corners, buffer):
        # Make every orientation equally likely
        self.random_corner_orientation(corners + buffer)

        num_twists = 0
        for corner_location in corners:
            if self.corners[corner_location].is_oriented():
                n = 1 + int(2*random.random())
                self.corners[corner_location].rotate_clockwise(n)
                num_twists += n

        num_twists = num_twists % 3
        if num_twists == 0:
            return

        if buffer:
            self.corners[random.choice(buffer)].rotate_clockwise((- num_twists) % 3)
            return
        # See if there is any corner we can twist so that everything is disoriented and num_twists is a multiple of 3
        for corner_location in corners:
            corner = self.corners[corner_location]
            if corner.colors[num_twists] != corner.oriented_color_order[0]:
                corner.rotate_clockwise[(- num_twists) % 3]
                return
        # See if we can twist two corners to get them all disoriented
        twistable_corners = [corner_location for corner_location in corners if corner.colors[(-num_twists)%3] != corner.oriented_color_order[0]]
        if len(twistable_corners) >= 2:
            a, b = tuple(random.sample(twistable_corners, 2))
            self.corners[a].rotate_clockwise(num_twists)
            self.corners[b].rotate_clockwise(num_twists)
            return
        # Nothing worked. We can't disorient these corners.
        self.corners[random.choice(corners)].rotate_clockwise((-num_twists)%3)


if __name__ == "__main__":
    # test
    import scramble
    cube = Cube()
    # cube.derange([], ["UR", "UL"], [], ["UB"])
    cube.random_permutation(["URF", "UBR", "ULB", "UFL"], ["UF", "UB", "UR", "UL"])
    cube.arrange(["URF", "UBR", "ULB", "UFL"], [], [], ["UF", "UB", "UR", "UL"])
    perm = scramble.generate_state(str(cube))
    print(perm)