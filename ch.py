import tkinter as tk
from board import Example
##############
# A mainfile #
##############
DIM = (7,6)
# Creates a tkinter window and positions it on a screen
root = tk.Tk()
root.geometry("455x450+800+300")
root.resizable(False, False)

app = Example(DIM)

player = app.getPlayer()

label = tk.Label(text=player)

app.pack()
label.pack()
root.mainloop()