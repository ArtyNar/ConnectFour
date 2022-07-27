from cProfile import label
from email.mime import message
from multiprocessing import Event
from tkinter import Frame, Label, messagebox, Button
from computerAI import oneStepAgent, randomAgent, nStepAgent
import scoreCalculations

import time

# import sys
# import os

class Player:
        playerNum = 0
        score = [0,0]

class Board(Frame):
    def __init__(self, DIM):
        # The only way it worked. 
        # Had to create a player class to hold the value for a current player
        self.player = Player()
        self.currentPlayerLabel = Label()
        self.currentScoreLabel = Label()
        self.simulateButton = Button()

        super().__init__()
        self.matrix = [[0 for x in range(DIM[0])] for y in range(DIM[1])] 
        self.decodedMatrix = [[0 for x in range(DIM[0])] for y in range(DIM[1])] 
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

                l = self.GameLabel(self, text=" ", position=[i,j])
                
                l.grid(row=i, column=j)

                self.matrix[i][j] = l
        self.pack()

        # Configuring a bottom labels
        self.updateLabels()

        # Sets up a simulate button
        self.simulateButton.config(text="Simulate")
        self.simulateButton.bind("<Button>", self.simulate)

        # Packing all the footer stuff
        self.currentPlayerLabel.pack()
        self.currentScoreLabel.pack()
        self.simulateButton.pack()
   
    # Returns a current player number (0 or 1)
    def getPlayer(self):
        return self.player.playerNum

    # Updates the bottom labels
    def updateLabels(self):
        self.currentPlayerLabel.config(text= "Current player: " + str(self.player.playerNum))
        self.currentScoreLabel.config(text="Score: 0 = " + str(self.player.score[0]) + "\nScore: 1 = " + str(self.player.score[1]))
      
    # Creates a simulation of a game, with agents playing against one another 
    def simulate(self, event):
        oneStepAgent(event, self)

    
    # An inner class for each label on the board
    # Inner, since lables won't exist without the parent
    class GameLabel(Label):
        # A lock, that checks if the cell is already taken
        lock = 0
        # Just a default filling
        filledWith = -1

        def __init__(self, parent, text, position):
            # Sets the position
            self.parent = parent

            self.x = position[1]
            self.y = position[0]

            # Calles the Label constructor
            super().__init__(parent, text=text, bg="white", fg="black", width=7, height=3)

            # Binds the behaviour to a mousedown
            self.bind("<Button>", self.on_mouse_down)
            
        # Definces onclick behaviour
        def on_mouse_down(self, event):
            # To print which player the label is filled with
            # print(self.filledWith)

            # I can see the coordinates of every cell I click 
            # self.printCoordinates()

            # This is how I can access the parent's variables. Awesome!!!
            # print("Player: ", self.parent.player.playerNum)

            # Check if the cell is already locked
            if self.lock == 0:
                # Checks if a position is allowed
                if self.checkIfCorrect():
                    # Decides the color to fill in
                    if self.parent.player.playerNum == 0:
                        self.parent.player.playerNum = 1
                        self.config(background="Blue")

                        # Updates the matrix used by ai
                        self.parent.decodedMatrix[self.y][self.x] = 1

                        self.filledWith = 0
                    else:
                        self.parent.player.playerNum = 0
                        self.config(background="Green")

                        # Updates the matrix used by ai
                        self.parent.decodedMatrix[self.y][self.x] = 2

                        self.filledWith = 1

                    # Lock the... lock ;)
                    self.lock = 1
                    
                    self.checkWin()
                    # Update the bottom labels
                    self.parent.updateLabels()

                    # Now, it is computer's turn!!!
                    # Here, you can choose which algorithm the AI will use
                    if(self.parent.player.playerNum == 1):
                        oneStepAgent(event, self.parent)

                else:
                    # Jumps to a correct selection within the column.
                    self.parent.matrix[self.y+1][self.x].on_mouse_down(event)
            else:
                print("Locked")

            # Allows me to check the matrix after each turn
            # print(self.parent.decodedMatrix)

        # Prints coordinates of a pressed label
        def printCoordinates(self):
            # To print coordinates
            print("x:", self.x, "y:", self.y)

        # Returns if the label is filled or not
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

        # Returns whatever player the cell is filled with
        def getLablePlayer(self):
            return self.filledWith

        # Calculates the score for each player based on the placed chip
        def getScore(self, playerNum):
            scoreCalculations.setScore(self, playerNum)
            return self.parent.player.score[playerNum]

        # Prints players' scores, shows if any of the players won
        def checkWin(self):
            score = self.getScore(1-self.parent.player.playerNum)
            #print("Score for Player ", self.parent.player.playerNum, ":" , score)
            if (score == 4):
                messagebox.showinfo(title="Game over", message="Player " + str(1-self.parent.player.playerNum) + " won!")

                # Returns a player that won
                return 1-self.parent.player.playerNum
        
        ###
        #
        #   The next set of functions is used to 
        #   calculate the score after each turn of the game.
        #   We have to check score horizontally, vertically, and diagonally.
        #   All of them are in the scoreCalculations.py library (?)
        #
        ###
        def setScore(self, playerNum):
            return scoreCalculations.setScore(self, playerNum)

        def checkRight(self, playerNum):
            return scoreCalculations.checkRight(self, playerNum)

        def checkLeft(self, playerNum):
            return scoreCalculations.checkLeft(self, playerNum)

        def checkDown(self, playerNum):
            return scoreCalculations.checkDown(self, playerNum)

        def checkDiagonal(self, playerNum):
            return scoreCalculations.checkDiagonal(self, playerNum)
