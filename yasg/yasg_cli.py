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
    op_group = optparse.OptionGroup(parser, "Orientation/Permutation options", "Used to specify the orientation an permutation of specific patterns.")
    parser.add_option_group(op_group)
    patterns_group = optparse.OptionGroup(parser, "Pattern options", "Used to get specific patterns to appear on the scramble without manipulating individual pieces.")
    parser.add_option_group(patterns_group)

    predefined_scramble_group.add_option("-s", "--step", dest="step", help="Generate a scramble for a given cube state. The predefined options are "
                           "LL, OLL, OLLCP, PLL, CLL, ELL, ZBLL, 2GLL, OCLL, COLL, EPLL, CPLL, CMLL, CMLLEO, ZZLL, F2L, ZZF2L, PetrusF2L, ZZRB, SB, "
                           "LS, ZZLS, CLS, ELS, CPLS, EJLS, TSLE, TTLL, WV, SV, VHLS, VLS, Petrus2x2x3, PetrusEO")
    predefined_scramble_group.add_option("-f", "--file", dest="file",
                                         help="Executes a scramble type specified in the YASG language. Use a path name to the file in which this scramble type is specified.")

    op_group.add_option("-p", "--permutable", dest="permutable_pieces", help="The pieces that could be permuted. Use this option as -p \"(all the corners that can be permuted, separated by spaces) | (edges, separated by spaces)\". To permute all the corners or edges, you can type \"all\" instead of a list of pieces. You don't have to use this option if all the corners and all the edges can be permuted. If no corners or no edges should be permuted, type \"\" in the section for the corners or edges. To permute all the corners in an (outer) layer, just type the symbol for that layer.")
    op_group.add_option("-o", "--orientable", dest="orientable_pieces", help="The pieces that could be disoriented. This works exacly the same as the -p option.")

    op_group.add_option("-A", "--arrange", dest="arranged_pieces", help="Correctly permute these pieces if they would be permuted incorrectly by another option. Syntax is the same as --permutable. Because not every permutation of the pieces is possible, it is advised to specify the pieces whose permutation you don't care about with the --permutable option. ")
    op_group.add_option("-O", "--orient", dest="oriented_pieces", help="Correctly orient these pieces if they would be permuted incorrectly by another option. Syntax is the same as --orientable. Because not every orientation of the pieces is possible, it is advised to specify the pieces whose orientation you don't care about with the --orientable option. ")
    op_group.add_option("-D", "--derange", dest="deranged_pieces", help="Put these pieces in a spot where they don't belong. See --arrange and --permutable for more information.")
    op_group.add_option("-d", "--disorient", dest="disoriented_pieces", help="Ensure that these pieces are disoriented. See --orient and --orientable for more information.")


    patterns_group.add_option("-e", "--badedges", dest="num_bad_edges", help="The exact number of bad edges, distributed randomly around the cube. Do not use this in combination with -o.")
    patterns_group.add_option("-c", "--ocll", dest="ocll", help="The corner orientation case in the last layer. This overrides every other method of orienting corners. Possible options are T, U, L, H, Pi, S, AS. You can list multiple possibilities, delimited by spaces. If this option isn't used, any case could be generated (unless CO is restricted by another option) ")
    patterns_group.add_option("-a", "--auf", action="store_true", dest="auf", help="Adds a random AUF at the end if used.")
    patterns_group.add_option("--pre", "--premoves", dest="pre_moves", help="Apply this algorithm before scrambling. These exact moves may not be visible in the scramble algorithm, but their effect will be.")
    patterns_group.add_option("--post", "--postmoves", dest="post_moves", help="Apply this algorithm after scrambling. These exact moves may not be visible in the scramble algorithm, but their effect will be.")
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
        if options.permutable_pieces:
            scramble_commands.permutable(cube, options.permutable_pieces)
        elif not options.arranged_pieces and not options.deranged_pieces:
            cube.random_permutation(Cube.corner_locations, cube.edge_locations)

        if options.orientable_pieces:
            scramble_commands.orientable(cube, options.orientable_pieces)
        elif not options.oriented_pieces and not options.disoriented_pieces and not options.ocll:
            cube.random_corner_orientation(Cube.corner_locations)
            cube.random_edge_orientation(Cube.edge_locations)

        if options.num_bad_edges:
            cube.flip_n_edges(Cube.edge_locations, int(options.num_bad_edges))

    if options.num_bad_edges:
        scramble_commands.n_bad_edges(cube, options.num_bad_edges)

    if options.deranged_pieces:
        if options.permutable_pieces:
            scramble_commands.derange(cube, options.deranged_pieces, options.permutable_pieces)
        else:
            scramble_commands.derange(cube, options.deranged_pieces)
    elif options.arranged_pieces:
        if options.permutable_pieces:
            scramble_commands.arrange(cube, options.arranged_pieces, options.permutable_pieces)
        else:
            scramble_commands.arrange(cube, options.arranged_pieces)
    if options.disoriented_pieces:
        if options.orientable_pieces:
            scramble_commands.disorient(cube, options.disoriented_pieces, options.orientable_pieces)
        else:
            scramble_commands.disorient(cube, options.disoriented_pieces)
    elif options.oriented_pieces:
        if options.orientable_pieces:
            scramble_commands.orient(cube, options.oriented_pieces, options.orientable_pieces)
        else:
            scramble_commands.orient(cube, options.oriented_pieces)

    if options.ocll:
        scramble_commands.twist_ll_corners(cube, options.ocll)
    if options.post_moves:
        cube.apply_algorithm(options.post_moves)
    if options.auf:
        cube.randomAUF()

    print(scramble.generate_state(str(cube)))



if __name__ == "__main__":
    main()
