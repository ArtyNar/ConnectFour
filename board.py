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

        for i in range(DIM[1]):
            for j in range(DIM[0]):
                self.matrix[i][j] = 0
                l = Label(self, text=self.matrix[i][j], bg="white", fg="black")
                l.grid(row=i, column=j)

                # Define Behaviour
                self.LabelOnClick(l, i, j)
        self.pack()


    def LabelOnClick(self, l, i, j):
        l.bind("<Button-1>", lambda e:print(i, j))
   

