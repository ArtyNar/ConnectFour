from cProfile import label
from multiprocessing import Event
from tkinter import Frame, Label, Button

class Player:
        playerNum = 0

class Example(Frame):

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

                l = self.MyLabel(self, self.player, text="emt", position=[i,j])
                
                l.grid(row=i, column=j)

                self.matrix[i][j] = l

        self.pack()
   
    def getPlayer(self):
        return self.player.playerNum

    class MyLabel(Label):
        lock = 0

        def __init__(self, parent, player, text, position):
            # Sets the position
            self.x = position[0]
            self.y = position[1]

            # Calles the Label constructor
            super().__init__(parent, text=text, bg="white", fg="black", width=7, height=3)

            # Binds the behaviour
            self.bind("<Button>", lambda event, arg=player: self.on_mouse_down(event, arg))
            
        # Definces onclick behaviour
        def on_mouse_down(self, event, player):
            print(self.x, self.y)
            print(player.playerNum)

            if self.lock == 0:
                if player.playerNum == 0:
                    player.playerNum = 1
                    self.config(background="Blue")
                else:
                    player.playerNum = 0
                    self.config(background="Green")

                self.lock = 1
            else:
                print("Locked")

