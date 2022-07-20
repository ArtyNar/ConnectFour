import random 
import copy
import numpy as np

# Mindless random agent, plots the chips randomly
def randomAgent(event, self):
    print("Random")

    valid_moves = [col for col in range(7) if self.parent.matrix[0][col].isFilled() == False]
    choiceCol = random.choice(valid_moves)

    self.parent.matrix[0][choiceCol].on_mouse_down(event)

###
# A better agent, looking one step ahead
# One-step lookahead agent will:
# - use the heuristic to assign a score to each possible valid move, and
# - select the move that gets the highest score. (If multiple moves get the high score, we select one at random.)
###
def betterAgent(event, self):
    print("Computer's turn!")
    # "Simply" chooses a valid move
    valid_moves = [col for col in range(7) if self.parent.matrix[0][col].isFilled() == False]

    # Makes a copy of a matrix to simulate
    matrixCopy = copy.deepcopy(self.parent.decodedMatrix)    

    choiceCol = 0

    matrixCopy = simulateDrop(matrixCopy, choiceCol)
    print(matrixCopy[:, 1, None], "\n")

    score = getScore(matrixCopy)
    print(score)

    #self.parent.matrix[0][choiceCol].on_mouse_down(event)

def simulateDrop(matrixCopy, colChoice):
    # Finds the valid row 
    for row in range(6-1, -1, -1):
        if matrixCopy[row][colChoice] == 0:
            break

    matrixCopy[row][colChoice] = 2
    return matrixCopy

def getScore(matrixCopy):
    num_threes = count_windows(matrixCopy, 3, rows=6, columns=7)
    return num_threes

# Helper function for get_heuristic: counts number of windows satisfying specified heuristic conditions
def count_windows(grid, num_discs, rows, columns):
    num_windows = 0
    # horizontal
    for row in range(rows):
        for col in range(4):
            window = list(grid[row][col:col+4])
            if check_window(window, num_discs):
               num_windows += 1

    # # vertical
    for col in range(6):
        for row in range(3):
            window = list(grid[row:row+3][0])
            #print(window)
            if check_window(window, num_discs):
                num_windows += 1
    
    # # positive diagonal
    # for row in range(rows-(4-1)):
    #     for col in range(columns-(4-1)):
    #         window = list(grid[range(row, row+4), range(col, col+4)])
    #         if check_window(window, num_discs):
    #             num_windows += 1
    # # negative diagonal
    # for row in range(4-1, rows):
    #     for col in range(columns-(4-1)):
    #         window = list(grid[range(row, row-4, -1), range(col, col+4)])
    #         if check_window(window, num_discs):
    #             num_windows += 1
    return num_windows

# Helper function for get_heuristic: checks if window satisfies heuristic conditions
def check_window(window, num_discs):
    return (window.count(2) == num_discs and window.count(0) == 4-num_discs)