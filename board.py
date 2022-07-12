from cProfile import label
from email.mime import message
from multiprocessing import Event
from tkinter import Frame, Label, messagebox
import sys
import os

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

                l = self.GameLabel(self, text="emt", position=[i,j])
                
                l.grid(row=i, column=j)

                self.matrix[i][j] = l
        self.pack()

        # Configuring a bottom labels
        self.updateLabels()

        self.currentPlayerLabel.pack()
        self.currentScoreLabel.pack()
   
    # Returns a current player number (0 or 1)
    def getPlayer(self):
        return self.player.playerNum

    def updateLabels(self):
        self.currentPlayerLabel.config(text= "Current player: " + str(self.player.playerNum))
        self.currentScoreLabel.config(text="Score: 0 = " + str(self.player.score[0]) + "\nScore: 1 = " + str(self.player.score[1]))
    
    
    # An inner class for each label on the board
    # Inner, since lables won't exist without the parent
    class GameLabel(Label):
        lock = 0
        filledWith = -1

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
            # To print which player the label is filled with
            #print(self.filledWith)

            #self.printCoordinates()

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

                        self.filledWith = 0
                    else:
                        self.parent.player.playerNum = 0
                        self.config(background="Green")

                        self.filledWith = 1

                    # Lock the... lock ;)
                    self.lock = 1

                    self.checkWin()
                    # Update the bottom labels
                    self.parent.updateLabels()
                else:
                    # Jumps to a correct selection within the column.
                    self.parent.matrix[self.y+1][self.x].on_mouse_down(event)
            else:
                print("Locked")

        def printCoordinates(self):
            # To print coordinates
            print("x:", self.x, "y:", self.y)

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

        # Calculates the score for each player
        def getScore(self, playerNum):
            self.setScore(playerNum)
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
        #
        ###
        def setScore(self, playerNum):
            horiz = self.checkRight(playerNum) + self.checkLeft(playerNum) - 1
            vert = self.checkDown(playerNum) 
            diag = self.checkDiagonal(playerNum)
            self.parent.player.score[playerNum] = max(horiz, vert, diag)
            
            return self.parent.player.score[playerNum]

        def checkRight(self, playerNum):
            if(self.filledWith != playerNum):
                return 0   
            if (self.x == 6):
                return 1
            return 1 + self.parent.matrix[self.y][self.x+1].checkRight(playerNum) 
        
        def checkLeft(self, playerNum):
            if(self.filledWith != playerNum):
                return 0
            if (self.x == 0):
                return 1
            return 1 + self.parent.matrix[self.y][self.x-1].checkLeft(playerNum) 

        def checkDown(self, playerNum):
            if(self.filledWith != playerNum):
                return 0
            if (self.y == 5):
                return 1
            return 1 + self.parent.matrix[self.y+1][self.x].checkDown(playerNum) 

        def checkDiagonal(self, playerNum):
            # Checking top left
            x = self.x
            y = self.y
            scoreTopLeft = 1
            while(True):
                x -= 1
                y -= 1
                if(x < 0 or y < 0):
                    break
                if(self.parent.matrix[y][x].filledWith != playerNum):
                    break
                else:
                    scoreTopLeft += 1

            # Checking bottom right
            x = self.x
            y = self.y
            scoreBottomRight = 1
            while(True):
                x += 1
                y += 1
                if(x > 6 or y > 5):
                    break
                if(self.parent.matrix[y][x].filledWith != playerNum):
                    break
                else:
                    scoreBottomRight += 1

            diagonal1 = scoreTopLeft + scoreBottomRight - 1
            
             # Checking top right
            x = self.x
            y = self.y
            scoreTopRight = 1
            while(True):
                x += 1
                y -= 1
                if(x > 6 or y < 0):
                    break
                if(self.parent.matrix[y][x].filledWith != playerNum):
                    break
                else:
                    scoreTopRight += 1

            # Checking bottom left
            x = self.x
            y = self.y
            scoreBottomLeft = 1
            while(True):
                x -= 1
                y += 1
                if(x < 0 or y > 5):
                    break
                if(self.parent.matrix[y][x].filledWith != playerNum):
                    break
                else:
                    scoreBottomLeft += 1

            diagonal2 = scoreTopRight + scoreBottomLeft - 1

            return max(diagonal1, diagonal2)
