import tkinter as tk
from board import Example
##############
# A mainfile #
##############
DIM = (7,6)
# Creates a tkinter window and positions it on a screen
root = tk.Tk()
root.geometry("500x500+800+300")
root.resizable(False, False)

# Run the app
app = Example(DIM)
root.mainloop()