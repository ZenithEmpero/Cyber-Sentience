import tkinter as tk
from settings import *


show_collision_box = SCB
def scb():
      global show_collision_box
      show_collision_box = True
      print(show_collision_box)

def sec_win():
    if second_window:
            sw = tk.Tk() # SECOND WINDOW
            sw.geometry(sw_size)

            button1 = tk.Button(master=sw, text="Show collision box", command= scb)
            button1.pack()

            sw.mainloop()