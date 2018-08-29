from optparse import OptionParser
from cube import *
import scramble

def main():
    optpar = OptionParser()
    optpar.add_option("--cp", dest="cp", help="The corners that can be permuted. If no corners should be permuted, type \"\".")
    optpar.add_option("--co", dest="co", help="The corners that can be disoriented. If no corners should be disoriented, type \"\".")
    optpar.add_option("--ep", dest="ep", help="The edges that can be permuted. If no edges should be permuted, type \"\".")
    optpar.add_option("--eo", dest="eo", help="The edges that can be disoriented. If no corners should be disoriented, type \"\".")

    (options, args) = optpar.parse_args()

    split = lambda s : s.split(" ") if s else s


    if options.cp is None:
        options.cp = Cube.corner_locations
    else:
        options.cp = [parse_corner_id(corner) for corner in split(options.cp)]
    if options.co is None:
        options.co = Cube.corner_locations
    else:
        options.co = [parse_corner_id(corner) for corner in split(options.co)]
    if options.ep is None:
        options.ep = Cube.edge_locations
    else:
        options.ep = [parse_edge_id(edge) for edge in split(options.ep)]
    if options.eo is None:
        options.eo = Cube.edge_locations
    else:
        options.eo = [parse_edge_id(edge) for edge in split(options.eo)]

    cube = Cube()
    cube.random_permutation(options.cp, options.ep)
    cube.random_corner_orientation(options.co)
    cube.random_edge_orientation(options.eo)
    print(scramble.generate_state(str(cube)))



if __name__ == "__main__":
    main()