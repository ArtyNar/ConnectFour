from cProfile import label
from tkinter import Frame, Label, Button

class Example(Frame):

    def __init__(self, DIM):
        super().__init__()
        self.matrix = [[0 for x in range(DIM[0])] for y in range(DIM[1])] 
        self.initUI(DIM)

    def initUI(self, DIM):
        self.master.title("Board")
        self.config(bg="black")

        # Adds Padding
        for i in range(DIM[0]):
            self.columnconfigure(i, pad=3)
        for i in range(DIM[1]):
            self.rowconfigure(i, pad=3)

        # Adds the labels to the grid
        for i in range(DIM[1]):
            for j in range(DIM[0]):
                self.matrix[i][j] = 0

                l = MyLabel(self, text="emt", position=[i,j])
                l.grid(row=i, column=j)

        self.pack()
   

class MyLabel(Label):
    def __init__(self, parent, text, position):
        # Sets the position
        self.x = position[0]
        self.y = position[1]

        # Calles the Label constructor
        super().__init__(parent, text=text, bg="white", fg="black", width=7, height=3)

        # Binds the behaviour
        self.bind("<Button>", self.click)

    # onClick behaviour
    def click(self, event):
        print(self.x, self.y)