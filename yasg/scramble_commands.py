from cube import *
import random

# Convert the user input to a list of pieces
# @param pieces: the input provided by the user
# @param correct_notation: the function that can correct the notation of an individual piece (e.g. BU --> UB)
# @default_pieces: all corner pieces if this is called on a list of corner pieces, or all edge pieces if this is called on a list of edge pieces
def parse_pieces_same_type(pieces, correct_notation, default_pieces):
    if pieces is None or pieces.lower() in ["all", "each", "every", "any"]:
        return default_pieces
    if not pieces:
        return []
    pieces = pieces.split(" ")
    scrambled_pieces = set([])
    for piece_symbol in pieces:
        if not piece_symbol:
            # this is a blank
            continue
        if len(piece_symbol) == 1:
            # The user wants to scramble the entire layer. Add all the pieces in this layer
            scrambled_pieces.update([piece for piece in default_pieces if piece_symbol[0] in piece])
        else:
            scrambled_pieces.add(correct_notation(piece_symbol))
    return list(scrambled_pieces)

def parse_pieces_input(input):
    (corners, edges) = tuple(input.split("|"))
    return (parse_pieces_same_type(corners, parse_corner_id, Cube.corner_locations),
            parse_pieces_same_type(edges, parse_edge_id, Cube.edge_locations))

def permutable(cb : Cube, args : str):
    cb.random_permutation(*parse_pieces_input(args))

def orientable(cb : Cube, args : str):
    corners, edges = parse_pieces_input(args)
    cb.random_corner_orientation(corners)
    cb.random_edge_orientation(edges)

def arrange(cb : Cube, arrange_args, buffer_args = " | "):
    cb.arrange(*parse_pieces_input(arrange_args), *parse_pieces_input(buffer_args))

def derange(cb : Cube, derange_args, buffer_args = " | "):
    cb.derange(*parse_pieces_input(derange_args), *parse_pieces_input(buffer_args))

def orient(cb : Cube, orient_args, buffer_args = " | "):
    corners, edges = parse_pieces_input(orient_args)
    buffer_corners, buffer_edges = parse_pieces_input(buffer_args)
    cb.orient_corners(corners, buffer_corners)
    cb.orient_edges(edges,buffer_edges)

def disorient(cb : Cube, disorient_args, buffer_args = " | "):
    corners, edges = parse_pieces_input(disorient_args)
    buffer_corners, buffer_edges = parse_pieces_input(buffer_args)
    cb.disorient_corners(corners, buffer_corners)
    cb.disorient_edges(edges, buffer_edges)

def n_bad_edges(cb : Cube, args):
    n = int(args)
    cb.orient_edges(Cube.edge_locations, [])
    cb.flip_n_edges(Cube.edge_locations, n)

_U_corners  = parse_pieces_same_type("U", parse_corner_id, Cube.corner_locations)
_U_edges    = parse_pieces_same_type("U", parse_edge_id, Cube.edge_locations)
_LS_corners = parse_pieces_same_type("U DFR", parse_corner_id, Cube.corner_locations)
_LS_edges   = parse_pieces_same_type("U FR", parse_edge_id, Cube.edge_locations)

# Set the values of cp, co, ep, and eo depending on the value of step
def set_step(cube : Cube, step : str):
    if step in ["LL", "OLL", "CLL", "OLLCP"]:
        cube.random_permutation(_U_corners, _U_edges)
        cube.random_edge_orientation(_U_edges)
        cube.random_corner_orientation(_U_corners)
    elif step == "PLL":
        cube.random_permutation(_U_corners, _U_edges)
    elif step in ["COLL", "ZBLL", "OCLL"]:
        cube.random_permutation(_U_corners, _U_edges)
        cube.random_corner_orientation(_U_corners)
    elif step == "2GLL":
        cube.randomAUF()
        cube.random_permutation([], _U_edges)
        cube.random_corner_orientation(_U_corners)
    elif step == "ELL":
        cube.random_permutation([], _U_edges)
        cube.random_edge_orientation(_U_edges)
    elif step == "EPLL":
        cube.random_permutation([], _U_edges)
    elif step == "CPLL":
        cube.random_permutation(_U_corners, [])
    elif step in ["CMLL", "CMLLEO"]:
        edges = parse_pieces_same_type("U DF DB", parse_edge_id, Cube.edge_locations)
        cube.random_permutation(_U_corners, edges)
        cube.random_corner_orientation(_U_corners)
        cube.random_edge_orientation(edges)
    elif step == "ZZLL":
        # If you just do "permute two edges and two corners", the probabilities don't quite match up.
        phase_edges = parse_pieces_same_type("UF UB", parse_edge_id, Cube.edge_locations)
        cube.random_permutation(_U_corners, phase_edges)
        cube.random_corner_orientation(_U_corners)
        cube.randomAUF() # the phase edges can also be on the side.
    elif step == "F2L":
        edges = parse_pieces_same_type("U FR FL BR BL", parse_edge_id, Cube.edge_locations)
        cube.random_permutation(Cube.corner_locations, edges)
        cube.random_corner_orientation(Cube.corner_locations)
        cube.random_edge_orientation(edges)
    elif step == "ZZF2L":
        edges = parse_pieces_same_type("R U L", parse_edge_id, Cube.edge_locations)
        cube.random_permutation(Cube.corner_locations, edges)
        cube.random_corner_orientation(Cube.corner_locations)
    elif step in ["ZZRB", "PetrusF2L"]:
        corners = parse_pieces_same_type("R U", parse_corner_id, Cube.corner_locations)
        edges = parse_pieces_same_type("R U", parse_edge_id, Cube.edge_locations)
        cube.random_permutation(corners, edges)
        cube.random_corner_orientation(corners)
    elif step == "SB":
        corners = parse_pieces_same_type("R U", parse_edge_id, Cube.corner_locations)
        edges = parse_pieces_same_type("R U DF DB", parse_edge_id, Cube.edge_locations)
        cube.random_permutation(corners, edges)
        cube.random_corner_orientation(corners)
        cube.random_edge_orientation(edges)
    elif step in ["LS", "ELS"]:
        cube.random_permutation(_LS_corners, _LS_edges)
        cube.random_corner_orientation(_LS_corners)
        cube.random_edge_orientation(_LS_edges)
    elif step in ["ZZLS", "TSLE"]:
        cube.random_permutation(_LS_corners,  _LS_edges)
        cube.random_corner_orientation(_LS_corners)
    elif step in ["CLS", "CPLS"]:
        cube.random_permutation(_LS_corners, _U_edges)
        cube.random_corner_orientation(_LS_corners)
    elif step in ["EJLS", "EJF2L"]:
        cube.random_permutation(_U_corners, _U_edges)
        cube.random_corner_orientation(_LS_corners)
        cube.disorient_corners(["DFR"], _U_corners)
    elif step == "TTLL":
        cube.random_permutation(_LS_corners, _U_edges)
    elif step == "WV":
        cube.random_permutation(_U_corners, _U_edges)
        cube.random_corner_orientation(_U_corners)
        cube.apply_algorithm("R U R'")
    elif step == "SV":
        cube.random_permutation(_U_corners, _U_edges)
        cube.random_corner_orientation(_U_corners)
        cube.apply_algorithm("R U\' R\'")
    elif step in ["VLS", "VHLS"]:
        cube.random_permutation(_U_corners, _U_edges)
        cube.random_corner_orientation(_U_corners)
        cube.random_edge_orientation(_U_edges)
        cube.apply_algorithm("R U\' R\'")
    elif step == "Petrus2x2x3":
        corners, edges = parse_pieces_input("U R F | U R F")
        cube.random_permutation(corners, edges)
        cube.random_corner_orientation(corners)
        cube.random_edge_orientation(edges)
    elif step == "PetrusEO":
        corners, edges = parse_pieces_input("U F | U F")
        cube.random_permutation(corners, edges)
        cube.random_corner_orientation(corners)
        cube.random_edge_orientation(edges)
    else:
        raise ValueError("Could not recognise the given step.")


def twist_ll_corners(cube, possible_cases):
    cube.orient_U_corners()
    case_name = random.choice(possible_cases.split(" "))
    if case_name.lower() == "t":
        cube.corners["ULB"].rotate_clockwise(1)
        cube.corners["UBR"].rotate_clockwise(2)
    elif case_name.lower() == "u":
        cube.corners["ULB"].rotate_clockwise(2)
        cube.corners["UBR"].rotate_clockwise(1)
    elif case_name.lower() == "l":
        cube.corners["ULB"].rotate_clockwise(2)
        cube.corners["URF"].rotate_clockwise(1)
    elif case_name.lower() == "h":
        cube.corners["ULB"].rotate_clockwise(1)
        cube.corners["UBR"].rotate_clockwise(2)
        cube.corners["URF"].rotate_clockwise(1)
        cube.corners["UFL"].rotate_clockwise(2)
    elif case_name.lower() in ["pi", "bruno"]:
        cube.corners["ULB"].rotate_clockwise(1)
        cube.corners["UFL"].rotate_clockwise(2)
        cube.corners["UBR"].rotate_clockwise(1)
        cube.corners["URF"].rotate_clockwise(2)
    elif case_name.lower() in ["s", "sune"]:
        cube.corners["URF"].rotate_clockwise(2)
        cube.corners["UBR"].rotate_clockwise(2)
        cube.corners["ULB"].rotate_clockwise(2)
    elif case_name.lower() in ["as", "antisune", "anti-sune"]:
        cube.corners["URF"].rotate_clockwise(1)
        cube.corners["UFL"].rotate_clockwise(1)
        cube.corners["ULB"].rotate_clockwise(1)
    elif case_name.lower() not in ["0", "o", "solved"]:
        raise(ValueError("OCLL case not recognised"))
    cube.randomAUF()