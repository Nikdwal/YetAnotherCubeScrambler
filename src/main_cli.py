#!/usr/bin/python3

from optparse import OptionParser
from cube import *
import scramble
import random
from scramble_commands import *

def main():
    optpar = OptionParser()
    optpar.add_option("--cp", dest="cp", help="The corners that can be permuted. You don't have to use this option if all corners can be permuted. If no corners should be permuted, type \"\". To permute all corners in a layer, just type the symbol for that layer.")
    optpar.add_option("--co", dest="co", help="The corners that can be disoriented. You don't have to use this option if all corners can be disoriented. If no corners should be disoriented, type \"\". To disorient all corners in a layer, just type the symbol for that layer.")
    optpar.add_option("--ep", dest="ep", help="The edges that can be permuted. You don't have to use this option if all edges can be permuted. If no edges should be permuted, type \"\". To permute all edges in a layer, just type the symbol for that layer.")
    optpar.add_option("--eo", dest="eo", help="The edges that can be disoriented. You don't have to use this option if all edges can be disoriented. If no corners should be disoriented, type \"\". To disorient all edges in a layer, just type the symbol for that layer.")
    optpar.add_option("-e", "--badedges", dest="num_bad_edges", help="The exact number of bad edges, distributed randomly around the cube. This overrides whatever is specified in --eo.")
    optpar.add_option("-s", "--step", dest="step", help="Generate a scramble for a given cube state. This step overrides --cp, --co, --ep, and --eo. Supported options are "
                                                        "LL, OLL, OLLCP, PLL, CLL, ELL, ZBLL, 2GLL, OCLL, COLL, EPLL, CPLL, CMLL, F2L, ZZF2L, PetrusF2L, ZZRB, SB, "
                                                        "LS, ZZLS, CLS, ELS, CPLS, EJLS, TSLE, TTLL. Custom scrambles can be generated with --cp, --co, --ep, and --eo.")
    optpar.add_option("-c", "--ocll", dest="ocll", help="The corner orientation case in the last layer. This overrides --co. Possible options are T, U, L, H, Pi, S, AS. You can list multiple possibilities, delimited by spaces. If this flag isn't used, any case could be generated (unless CO is restricted by another option) ")
    (options, args) = optpar.parse_args()

    if options.step is None:
        # No step specified, go with the specific pieces the user indicated
        options.cp = parse_pieces_same_type(options.cp, parse_corner_id, Cube.corner_locations)
        options.co = parse_pieces_same_type(options.co, parse_corner_id, Cube.corner_locations)
        options.ep = parse_pieces_same_type(options.ep, parse_edge_id, Cube.edge_locations)
        options.eo = parse_pieces_same_type(options.eo, parse_edge_id, Cube.edge_locations)
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