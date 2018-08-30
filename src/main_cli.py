#!/usr/bin/python3

import optparse
from cube import *
import scramble
import scramble_commands
from interpreter import Interpreter

def main():
    parser = optparse.OptionParser()
    predefined_scramble_group = optparse.OptionGroup(parser, "Predefined scrambles", "Use these options to generate scrambles for a predefined step or a step you have specified before.")
    parser.add_option_group(predefined_scramble_group)
    scramble_building_group = optparse.OptionGroup(parser, "On-the-fly scramble specifications", "Options to quickly specify a new type of scramble.")
    parser.add_option_group(scramble_building_group)

    predefined_scramble_group.add_option("-s", "--step", dest="step", help="Generate a scramble for a given cube state. The predefined options are "
                           "LL, OLL, OLLCP, PLL, CLL, ELL, ZBLL, 2GLL, OCLL, COLL, EPLL, CPLL, CMLL, CMLLEO, ZZLL, F2L, ZZF2L, PetrusF2L, ZZRB, SB, "
                           "LS, ZZLS, CLS, ELS, CPLS, EJLS, TSLE, TTLL, WV, SV, VHLS, VLS, Petrus2x2x3, PetrusEO")
    predefined_scramble_group.add_option("-f", "--file", dest="file",
                                         help="Executes a scramble type specified in the YASG language. Use a path name to the file in which this scramble type is specified.")
    scramble_building_group.add_option("-p", "--permute", dest="permuted_pieces", help="The pieces that can be permuted. Use this option as -p \"(all the corners that can be permuted, separated by spaces) | (edges, separated by spaces)\". To permute all the corners or edges, you can type \"all\" instead of a list of pieces. You don't have to use this option if all the corners and all the edges can be permuted. If no corners or no edges should be permuted, type \"\" in the section for the corners or edges. To permute all the corners in an (outer) layer, just type the symbol for that layer.")
    scramble_building_group.add_option("-o", "--disorient", dest="disoriented_pieces", help="The pieces that can be disoriented. This works exacly the same as the -p option.")
    scramble_building_group.add_option("-e", "--badedges", dest="num_bad_edges", help="The exact number of bad edges, distributed randomly around the cube. Do not use this in combination with -o.")
    scramble_building_group.add_option("-c", "--ocll", dest="ocll", help="The corner orientation case in the last layer. Do not use this in combination with -o. Possible options are T, U, L, H, Pi, S, AS. You can list multiple possibilities, delimited by spaces. If this option isn't used, any case could be generated (unless CO is restricted by another option) ")
    scramble_building_group.add_option("-a", "--auf", action="store_true", dest="auf", help="Adds a random AUF at the end if used.")
    scramble_building_group.add_option("--pre", "--premoves", dest="pre_moves", help="Apply this algorithm before scrambling. These exact moves may not be visible in the scramble algorithm, but their effect will be.")
    scramble_building_group.add_option("--post", "--postmoves", dest="post_moves", help="Apply this algorithm after scrambling. These exact moves may not be visible in the scramble algorithm, but their effect will be.")
    (options, args) = parser.parse_args()

    cube = Cube()

    if options.pre_moves:
        cube.apply_algorithm(options.pre_moves)

    if options.file:
        interpreter = Interpreter(options.file, cube)
        interpreter.execute_program()
    elif options.step:
        scramble_commands.set_step(cube, options.step)
    else:
        # Custom "on-the fly" scramble type

        if options.permuted_pieces:
            scramble_commands.permute(cube, options.permuted_pieces)
        else:
            cube.random_permutation(Cube.corner_locations, cube.edge_locations)

        if options.disoriented_pieces:
            scramble_commands.orient(cube, options.disoriented_pieces)
        elif options.ocll:
            scramble_commands.twist_ll_corners(cube, options.ocll)
        else:
            cube.random_corner_orientation(Cube.corner_locations)
            cube.random_edge_orientation(Cube.edge_locations)

        if options.num_bad_edges:
            cube.flip_n_edges(Cube.edge_locations, int(options.num_bad_edges))

        if options.auf:
            cube.randomAUF()

    if options.post_moves:
        cube.apply_algorithm(options.post_moves)

    print(scramble.generate_state(str(cube)))



if __name__ == "__main__":
    main()