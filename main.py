import tkinter as tk
from board import Board
##############
# A mainfile #
##############
DIM = (7,6)
# Creates a tkinter window and positions it on a screen
root = tk.Tk()
root.geometry("455x525+800+300")
root.resizable(False, False)

app = Board(DIM)
app.pack()

root.mainloop()

