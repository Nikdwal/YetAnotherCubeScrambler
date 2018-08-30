from tkinter import *
from cube import Cube
import scramble

root = Tk()

def generate_scramble(dummy_arg):
    cube = Cube()
    cube.random_corner_orientation(cube.corner_locations)
    cube.random_permutation(cube.corner_locations, [edge for edge in cube.edge_locations if edge not in ["DF", "DB"]])
    scramble_lbl.config(text="  " + scramble.generate_state(str(cube)) + "  ")
    scramble_lbl.pack()
    
root.bind("<space>", generate_scramble)

scramble_lbl = Label(root, font=("Noto Sans", 23))
scramble_lbl.pack()

generate_scramble(None)

mainloop()
