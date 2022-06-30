from cProfile import label
from multiprocessing import Event
from tkinter import Frame, Label, Button
from PIL import Image, ImageTk

class Player:
        playerNum = 0

class Board(Frame):

    def __init__(self, DIM):
        # The only way it worked. 
        # Had to create a player class to hold the value for a current player
        self.player = Player()
        self.cells = []

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

                l = self.MyLabel(self, text="emt", position=[i,j])
                
                l.grid(row=i, column=j)

                self.matrix[i][j] = l

        self.pack()
   
    def getPlayer(self):
        return self.player.playerNum
    
    
    # An inner class for each label on the board
    # Inner, since lables won't exist without the parent
    class MyLabel(Label):
        lock = 0

        def __init__(self, parent, text, position):
            # Sets the position
            self.parent = parent

            self.x = position[1]
            self.y = position[0]

            # Calles the Label constructor
            super().__init__(parent, text=text, bg="white", fg="black", width=7, height=3)

            # Binds the behaviour
            self.bind("<Button>", self.on_mouse_down)
            
        # Definces onclick behaviour
        def on_mouse_down(self, event):
            print("x:", self.x, "y:", self.y)

            # This is how I can access the parent's variables. Awesome!!!
            print("Player: ", self.parent.player.playerNum)

            # Check if the cell is already locked
            if self.lock == 0:
                # Checks if a position is allowed
                if self.checkIfCorrect():
                    # Decides the color to fill in
                    if self.parent.player.playerNum == 0:
                        self.parent.player.playerNum = 1
                        self.config(background="Blue")
                    else:
                        self.parent.player.playerNum = 0
                        self.config(background="Green")
                    self.lock = 1
                else:
                    print("Incorrect selection")
            else:
                print("Locked")

        def isFilled(self):
            if self.lock == 1:
                return True
            else:
                return False

        # This checks if a position of a new circle is viable
        def checkIfCorrect(self):
            filled = False
            
            # Here, we have to check a square underneath the selection.
            # If it is either the edge or a filled suqre underneath, the selection is legal
            if(self.y+1 == 6 or self.parent.matrix[self.y+1][self.x].isFilled()):
                filled = True

            return filled