from optparse import OptionParser
from cube import *
import scramble
import random

# Convert the user input to a list of pieces
# @param pieces: the input provided by the user
# @param correct_notation: the function that can correct the notation of an individual piece (e.g. BU --> UB)
# @default_pieces: all corner pieces if this is called on a list of corner pieces, or all edge pieces if this is called on a list of edge pieces
def parse_pieces_input(pieces, correct_notation, default_pieces):
    if pieces is None:
        return default_pieces
    if not pieces:
        return []
    pieces = pieces.split(" ")
    scrambled_pieces = set([])
    for piece_symbol in pieces:
        if len(piece_symbol) == 1:
            # The user wants to scramble the entire layer. Add all the pieces in this layer
            scrambled_pieces.update([piece for piece in default_pieces if piece_symbol[0] in piece])
        else:
            scrambled_pieces.add(correct_notation(piece_symbol))
    return list(scrambled_pieces)

# Set the values of options.cp, options.co, options.ep, and options.eo depending on the value of options.step
def set_step(options):
    if options.step in ["LL", "OLL", "CLL", "OLLCP"]:
        options.cp = parse_pieces_input("U", parse_corner_id, Cube.corner_locations)
        options.co = options.cp
        options.ep = parse_pieces_input("U", parse_edge_id, Cube.edge_locations)
        options.eo = options.ep
    elif options.step == "PLL":
        options.cp = parse_pieces_input("U", parse_corner_id, Cube.corner_locations)
        options.co = []
        options.ep = parse_pieces_input("U", parse_edge_id, Cube.edge_locations)
        options.eo = []
    elif options.step in ["COLL", "ZBLL", "OCLL"]:
        options.cp = parse_pieces_input("U", parse_corner_id, Cube.corner_locations)
        options.co = options.cp
        options.ep = parse_pieces_input("U", parse_edge_id, Cube.edge_locations)
        options.eo = []
    elif options.step == "2GLL":
        options.cp = []
        options.co = parse_pieces_input("U", parse_corner_id, Cube.corner_locations)
        options.ep = parse_pieces_input("U", parse_edge_id, Cube.edge_locations)
        options.eo = []
    elif options.step == "ELL":
        options.cp = []
        options.co = []
        options.ep = parse_pieces_input("U", parse_edge_id, Cube.edge_locations)
        options.eo = options.ep
    elif options.step == "EPLL":
        options.cp = []
        options.co = []
        options.eo = []
        options.ep = parse_pieces_input("U", parse_edge_id, Cube.edge_locations)
    elif options.step == "CPLL":
        options.cp = parse_pieces_input("U", parse_corner_id, Cube.corner_locations)
        options.co = []
        options.eo = []
        options.ep = []
    elif options.step == "CMLL":
        options.cp = parse_pieces_input("U", parse_corner_id, Cube.corner_locations)
        options.co = options.cp
        options.ep = parse_pieces_input("U DF DB", parse_edge_id, Cube.edge_locations)
        options.eo = options.ep
    elif options.step == "F2L":
        options.cp = Cube.corner_locations
        options.co = options.cp
        options.ep = parse_pieces_input("U FR FL BR BL", parse_edge_id, Cube.edge_locations)
        options.eo = options.ep
    elif options.step == "ZZF2L":
        options.cp = Cube.corner_locations
        options.co = options.cp
        options.ep = parse_pieces_input("R U L", parse_edge_id, Cube.edge_locations)
        options.eo = []
    elif options.step in ["ZZRB", "PetrusF2L"]:
        options.cp = parse_pieces_input("R U", parse_corner_id, Cube.corner_locations)
        options.co = options.cp
        options.ep = parse_pieces_input("R U", parse_edge_id, Cube.edge_locations)
        options.eo = []
    elif options.step == "SB":
        options.cp = parse_pieces_input("R U", parse_edge_id, Cube.corner_locations)
        options.co = options.cp
        options.ep = parse_pieces_input("R U DF DB", parse_edge_id, Cube.edge_locations)
        options.eo = []
    elif options.step in ["LS", "ELS"]:
        options.cp = parse_pieces_input("U DFR", parse_corner_id, Cube.corner_locations)
        options.co = options.cp
        options.ep = parse_pieces_input("U FR", parse_edge_id, Cube.edge_locations)
        options.eo = options.ep
    elif options.step in ["ZZLS", "TSLE"]:
        options.cp = parse_pieces_input("U DFR", parse_corner_id, Cube.corner_locations)
        options.co = options.cp
        options.ep = parse_pieces_input("U FR", parse_edge_id, Cube.edge_locations)
        options.eo = []
    elif options.step in ["CLS", "CPLS"]:
        options.cp = parse_pieces_input("U DFR", parse_corner_id, Cube.corner_locations)
        options.co = options.cp
        options.ep = parse_pieces_input("U", parse_edge_id, Cube.edge_locations)
        options.eo = []
    elif options.step in ["EJLS", "EJF2L"]:
        options.cp = parse_pieces_input("U", parse_corner_id, Cube.corner_locations)
        options.co = parse_pieces_input("U DFR", parse_corner_id, Cube.corner_locations)
        options.ep = parse_pieces_input("U", parse_edge_id, Cube.edge_locations)
        options.eo = []
    elif options.step == "TTLL":
        options.cp = parse_pieces_input("U DFR", parse_corner_id, Cube.corner_locations)
        options.co = []
        options.ep = parse_pieces_input("U", parse_edge_id, Cube.edge_locations)
        options.eo = []
    elif options.step == "2x2x2":
        options.cp = parse_pieces_input("U F R", parse_corner_id, Cube.corner_locations)
        options.co = options.cp
        options.ep = parse_pieces_input("U F R", parse_edge_id, Cube.edge_locations)
        options.eo = options.ep
    elif options.step == "2x2x3":
        options.cp = parse_pieces_input("U F", parse_corner_id, Cube.corner_locations)
        options.co = options.cp
        options.ep = parse_pieces_input("U F", parse_edge_id, Cube.edge_locations)
        options.eo = options.ep
    else:
        raise ValueError("Could not recognise the given step.")

def twist_ll_corners(cube, possible_cases):
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

def main():
    optpar = OptionParser()
    optpar.add_option("--cp", dest="cp", help="The corners that can be permuted. You don't have to use this option if all corners can be permuted. If no corners should be permuted, type \"\". To permute all corners in a layer, just type the symbol for that layer.")
    optpar.add_option("--co", dest="co", help="The corners that can be disoriented. You don't have to use this option if all corners can be disoriented. If no corners should be disoriented, type \"\". To disorient all corners in a layer, just type the symbol for that layer.")
    optpar.add_option("--ep", dest="ep", help="The edges that can be permuted. You don't have to use this option if all edges can be permuted. If no edges should be permuted, type \"\". To permute all edges in a layer, just type the symbol for that layer.")
    optpar.add_option("--eo", dest="eo", help="The edges that can be disoriented. You don't have to use this option if all edges can be disoriented. If no corners should be disoriented, type \"\". To disorient all edges in a layer, just type the symbol for that layer.")
    optpar.add_option("-e", "--badedges", dest="num_bad_edges", help="The exact number of bad edges, distributed randomly around the cube. This overrides whatever is specified in --eo.")
    optpar.add_option("-s", "--step", dest="step", help="Generate a scramble for a given cube state. This step overrides --cp, --co, --ep, and --eo. Supported options are "
                                                        "LL, OLL, OLLCP, PLL, CLL, ELL, ZBLL, 2GLL, OCLL, COLL, EPLL, CPLL, CMLL, F2L, ZZF2L, PetrusF2L, ZZRB, SB, "
                                                        "LS, ZZLS, CLS, ELS, CPLS, EJLS, TSLE, TTLL, 2x2x2, 2x2x3. Custom scrambles can be generated with --cp, --co, --ep, and --eo.")
    optpar.add_option("-c", "--ocll", dest="ocll", help="The corner orientation case in the last layer. This overrides --co. Possible options are T, U, L, H, Pi, S, AS. You can list multiple possibilities, delimited by spaces. If this flag isn't used, any case could be generated (unless CO is restricted by another option) ")
    (options, args) = optpar.parse_args()

    if options.step is None:
        # No step specified, go with the specific pieces the user indicated
        options.cp = parse_pieces_input(options.cp, parse_corner_id, Cube.corner_locations)
        options.co = parse_pieces_input(options.co, parse_corner_id, Cube.corner_locations)
        options.ep = parse_pieces_input(options.ep, parse_edge_id, Cube.edge_locations)
        options.eo = parse_pieces_input(options.eo, parse_edge_id, Cube.edge_locations)
    else:
        set_step(options)


    cube = Cube()
    cube.random_permutation(options.cp, options.ep)
    if options.ocll:
        twist_ll_corners(cube, options.ocll)
    else:
        cube.random_corner_orientation(options.co)
    if options.num_bad_edges:
        cube.flip_n_edges(Cube.edge_locations, int(options.num_bad_edges))
    else:
        cube.random_edge_orientation(options.eo)
    print(scramble.generate_state(str(cube)))



if __name__ == "__main__":
    main()