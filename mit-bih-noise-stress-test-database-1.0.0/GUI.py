import tkinter as tk
from tkinter import filedialog

def load_file():
    return filedialog.askopenfilename()


root = tk.Tk()
load = tk.Button(text = 'Load File', command = load_file)
print(load)
load.pack()
root.mainloop()
