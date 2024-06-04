from testcases import Testcases
import tkinter as tk
from tkinter import *
import copilot_calls
import asyncio
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk


root = tk.Tk()
root.grid_rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

frame_main = tk.Frame(root, bg="orange")
frame_main.grid(sticky='news')

image = Image.open("smith&nephew.png")
image = image.resize((int(image.width/2.2), int(image.height/2.2)))
photo = ImageTk.PhotoImage(image)
label = Label(root, image = photo)
label.image = photo
label.grid(row=0, sticky="n", rowspan=2)

settings = tk.Button(frame_main, text="Settings")
settings.grid(row=2, column=0)  # Start from row 2

upload = tk.Button(frame_main, text="Upload")
upload.grid(row=2, column=1)

generate = tk.Button(frame_main, text="Generate")
generate.grid(row=2, column=2)

export = tk.Button(frame_main, text="Export")  # Changed variable name to 'export'
export.grid(row=2, column=3)
root.mainloop()