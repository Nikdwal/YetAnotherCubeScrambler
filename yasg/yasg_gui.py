#!/usr/bin/python3

from tkinter import *
from tkinter import filedialog
import subprocess
import shlex
import os

curr_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(curr_directory)

root = Tk()
win = PanedWindow(root, orient=VERTICAL)
win.pack()
win.pack(fill=BOTH, expand=1)
root.title("YASG: Yet Another Scramble Generator")

top = PanedWindow(win, orient=HORIZONTAL)
win.add(top)

argbox = Entry(top, width=70)
top.add(argbox)

def generate_scramble():
    try:
        message = subprocess.check_output(["python", "yasg_cli.py"] + shlex.split(argbox.get())).decode("utf-8")[:-1]
    except subprocess.CalledProcessError:
        message = "Error. Check your input or file."

    scramble_lbl.config(state=NORMAL)
    scramble_lbl.delete(0,END)
    scramble_lbl.insert(END,message)
    scramble_lbl.config(state="readonly")
    scramble_lbl.pack()

def show_help():
    help_window = Tk()
    help_window.title("YASG Help")

    scrollbar = Scrollbar(help_window)
    scrollbar.pack(side=RIGHT, fill=Y)

    text = Text(help_window, wrap=WORD, yscrollcommand=scrollbar.set)

    text.insert(END,
                "To generate a custom scramble, type in some of the options below. You don\'t have "
                "to type in anything to get a completely random state.\n\n"
                "You can find a tutorial on the GitHub page for YASG: https://github.com/Nikdwal/YetAnotherScrambleGenerator\n\n\n")
    text.insert(END, subprocess.check_output(["python", "yasg_cli.py", "--help"]))
    text.config(state=DISABLED)
    text.pack()

    scrollbar.config(command=text.yview)
    # scramble_lbl.config(text="github.com/Nikdwal/YetAnotherScrambleGenerator")
    # scramble_lbl.pack()

def open_file():
    filename = filedialog.askopenfilename(initialdir=os.path.expanduser("~"), title="Select file",
                                               filetypes=(("YASG files", "*.yasg *.txt"), ("all files", "*.*")))
    argbox.delete(0, END)
    argbox.insert(0, "--file \"" + filename + "\"")
    generate_scramble()


scramble_section = Label(win)
win.add(scramble_section)

scramble_button = Button(top, text="Scramble", command=generate_scramble)
top.add(scramble_button)

open_button = Button(top, text="Open", command=open_file)
top.add(open_button)

help_button = Button(top, text="Help", command=show_help)
top.add(help_button)

scramble_lbl = Entry(scramble_section, font=("Sans Serif", 18), justify=CENTER, state="readonly", borderwidth=0, background=scramble_section["bg"])
scramble_lbl.pack(fill='x')

for widget in [argbox, scramble_lbl]:
    widget.bind("<Return>", lambda _ : generate_scramble())

# Set the minimum size to a size that fits the widgets
root.update()
root.minsize(root.winfo_width(), root.winfo_height())


top.grid_columnconfigure(0, weight=1)
top.grid_columnconfigure(3, weight=0)

mainloop()
