from cProfile import label
from email.mime import message
from multiprocessing import Event
from tkinter import Frame, Label, messagebox, Button
from computerAI import oneStepAgent, randomAgent
import scoreCalculations
from nstepAgent import nstepAgent

import time

# import sys
# import os

# Global scores for first, second players, and ties

class Player:
        playerNum = 0
        score = [0,0]

class Board(Frame):
    def __init__(self, DIM):
        # The only way it worked. 
        # Had to create a player class to hold the value for a current player
        self.DIM = DIM
        self.player = Player()
        self.currentPlayerLabel = Label()
        self.currentScoreLabel = Label()
        self.simulateGameButton = Button()
        self.simulateDropButton = Button()

        self.scores = [0,0,0]

        self.isWon = False
        self.isTie = False

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

        # Sets up simulate buttons
        self.simulateGameButton.config(text="Simulate Game")
        self.simulateGameButton.bind("<Button>", self.simulateManyGames)

        self.simulateDropButton.config(text="Simulate Drop")
        self.simulateDropButton.bind("<Button>", self.simulateDrop)

        # Packing all the footer stuff
        self.currentPlayerLabel.pack()
        self.currentScoreLabel.pack()
        self.simulateDropButton.pack()
        self.simulateGameButton.pack()
   
    # Returns a current player number (0 or 1)
    def getPlayer(self):
        return self.player.playerNum

    # Updates the bottom labels
    def updateLabels(self):
        self.currentPlayerLabel.config(text= "Current player: " + str(self.player.playerNum))
        self.currentScoreLabel.config(text="Score: 0 = " + str(self.scores[0]) + "\nScore: 1 = " + str(self.scores[1]) + "\nTies = " + str(self.scores[2]))
      
    # Creates a simulation of a game, with agents playing against one another 
    def simulateGame(self, event):
        while(self.isWon == False and self.isTie == False):
            oneStepAgent(event, self, self.player.playerNum)            # !!!! CHANGE THE ANGENT HERE
        # Having to now roll back the game status
        self.isWon = False
        self.isTie = False
        #self.reset()

    # Now the fun part - I can simulate many games to be played consecutively
    def simulateManyGames(self, event):
        for i in range(10):
            self.simulateGame(event)
    
    # Simulates a single drop using a particular agent
    def simulateDrop(self, event):
        oneStepAgent(event, self, self.player.playerNum)                  # !!!! CHANGE THE AGENT HERE

    # Resets the board to start the game over
    def resetAll(self):
        self.decodedMatrix = [[0 for x in range(self.DIM[0])] for y in range(self.DIM[1])] 
        self.player.playerNum = 0
        self.updateLabels()
        for rows in range(self.DIM[1]):
            for cols in range(self.DIM[0]):
                self.matrix[rows][cols].reset()

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
                    
                    # Update the bottom labels
                    self.parent.updateLabels()

                    # Increments the global score if the game is won
                    self.checkWin()

                    # # Here, I can make the computer's turn automatic if I want to
                    # if(not self.checkWin()):
                    #     if(self.parent.player.playerNum == 1):
                    #         nstepAgent(event, self.parent, self.parent.player.playerNum)                                    #!!!! CHANGE THE PLAYER 1 AGENT HERE
                else:
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

        # Resets a lable to the initial state
        def reset(self):
            self.lock = 0
            self.filledWith = -1
            self.config(background="White")

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
                #messagebox.showinfo(title="Game over", message="Player " + str(1-self.parent.player.playerNum) + " won!")
                self.parent.isWon = True
                
                #Increments the global score for the winner
                winnerPlayer = 1 - self.parent.player.playerNum
                self.parent.scores[winnerPlayer] +=1

                self.parent.resetAll()
                return True
            else: 
                return False

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
