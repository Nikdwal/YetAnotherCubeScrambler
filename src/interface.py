from tkinter import *
from cube import Cube
import scramble

root = PanedWindow(orient=VERTICAL)
root.pack(fill=BOTH, expand=1)

top = PanedWindow(root, orient=HORIZONTAL)
root.add(top)

cp = {corner: BooleanVar() for corner in Cube.corner_locations}
ep = {edge: BooleanVar() for edge in Cube.edge_locations}
co = {corner: BooleanVar() for corner in Cube.corner_locations}
eo = {edge: BooleanVar() for edge in Cube.edge_locations}

orient_section = Label(top)
top.add(orient_section)
orient_lbl = Label(orient_section, text="Disorient:")
orient_lbl.pack()
for corner in co:
    c = Checkbutton(orient_section, text=corner, onvalue=True, offvalue=False, variable=co[corner])
    c.pack()
for edge in eo:
    c = Checkbutton(orient_section, text=edge, onvalue=True, offvalue=False, variable=eo[edge])
    c.pack()

permute_section = Label(top)
top.add(permute_section)
permute_lbl = Label(permute_section, text="Permute:")
permute_lbl.pack()
for corner in co:
    c = Checkbutton(permute_section, text=corner, onvalue=True, offvalue=False, variable=cp[corner])
    c.pack()
for edge in eo:
    c = Checkbutton(permute_section, text=edge, onvalue=True, offvalue=False, variable=ep[edge])
    c.pack()

def generate_scramble():
    orient_edges = [edge for edge in eo if eo[edge].get()]
    permute_edges = [edge for edge in eo if ep[edge].get()]
    orient_corners = [corner for corner in co if co[corner].get()]
    permute_corners = [corner for corner in cp if cp[corner].get()]
    cube = Cube()
    cube.random_edge_orientation(orient_edges)
    cube.random_corner_orientation(orient_corners)
    cube.random_permutation(permute_corners, permute_edges)

    scramble_lbl.config(text=scramble.generate_state(str(cube)))
    scramble_lbl.pack()

scramble_section = Label(root)
root.add(scramble_section)

button = Button(scramble_section, text="scramble", command=generate_scramble)
button.pack()

scramble_lbl = Label(scramble_section, font=("Noto Sans", 23))
scramble_lbl.pack()

mainloop()
