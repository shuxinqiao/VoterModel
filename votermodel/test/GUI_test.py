import sys, os

# add path to parent directory
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from utils import *
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk


def submit_action():

    return 0


# initialization
root = tk.Tk()
root.title("Voter Model Simulator")

# window size
window_width = 800
window_height = 600
root.minsize(window_width, window_height)

# icon
program_directory = sys.path[0]
root.iconphoto(True, tk.PhotoImage(file=os.path.join(program_directory, "icon.PNG")))

# open position
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

center_x = int((screen_width - window_width)/2)
center_y = int((screen_height - window_height)/2)

root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

# grid config
#root.columnconfigure(0, weight=1)


# parameter frame
param = ttk.Frame(root)
param.grid(row=0)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)
root.columnconfigure(2, weight=1)

# graph frame
graph = ttk.Frame(root)
graph.grid(row=2)

# parameters - size n
size_n = tk.IntVar()

size_label = ttk.Label(param, text="Size of population (int):")
size_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

size_entry = ttk.Entry(param, textvariable=size_n)
size_entry.grid(column=1, row=0, sticky=tk.W, padx=5, pady=5)
size_entry.focus()

size_button = ttk.Button(param, text='Submit', compound=tk.LEFT, command=submit_action)
size_button.grid(column=2, row=0, sticky=tk.W, padx=10, pady=5)



root.mainloop()

