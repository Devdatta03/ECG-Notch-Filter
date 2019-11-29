import tkinter as tk
from tkinter import filedialog

root = tk.Tk(screenName='ECG Analyzer')
load_file = filedialog.askopenfilename()
print(load_file)
