#!/usr/bin/python3

from tkinter import *
import subprocess
import shlex
import os

curr_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(curr_directory)

root = PanedWindow(orient=VERTICAL)
root.pack(fill=BOTH, expand=1)
root.winfo_toplevel().title("YASG: Yet Another Scramble Generator")

top = PanedWindow(root, orient=HORIZONTAL)
root.add(top)

argbox = Entry(top, width=60)
top.add(argbox)

def generate_scramble():
    scramble_lbl.config(text=subprocess.check_output(["python", "main_cli.py"] + shlex.split(argbox.get())))
    scramble_lbl.pack()

def show_help():
    help_window = Tk()
    help_window.title("YASG Help")

    scrollbar = Scrollbar(help_window)
    scrollbar.pack(side=RIGHT, fill=Y)

    text = Text(help_window, wrap=WORD, yscrollcommand=scrollbar.set)

    text.insert(END,
                "To generate a custom scramble, type in some of the options below to generate a custom scramble. You don\'t have "
                "to type in anything to get a completely random state.\n\n"
                "You can find a tutorial on the GitHub page for YASG: https://github.com/Nikdwal/YetAnotherScrambleGenerator\n\n\n")
    text.insert(END, subprocess.check_output(["python", "main_cli.py", "--help"]))
    text.config(state=DISABLED)
    text.pack()

    scrollbar.config(command=text.yview)
    # scramble_lbl.config(text="github.com/Nikdwal/YetAnotherScrambleGenerator")
    # scramble_lbl.pack()

argbox.bind("<Return>", lambda _ : generate_scramble())

scramble_section = Label(root)
root.add(scramble_section)

scramble_button = Button(top, text="scramble", command=generate_scramble)
top.add(scramble_button)

help_button = Button(top, text="help", command=show_help)
top.add(help_button)

scramble_lbl = Label(scramble_section, font=("Noto Sans", 20))
scramble_lbl.pack()

mainloop()
