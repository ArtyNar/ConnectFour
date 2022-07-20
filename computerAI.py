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

    # Iterates over each potential chip drop, gets the score and stores all of them in an array
    results = []
    for col in valid_moves:
        # Makes a copy of a matrix to simulate
        matrixCopy = np.asarray(copy.deepcopy(self.parent.decodedMatrix))
        matrixCopy = simulateDrop(matrixCopy, col)
        score = getScore(matrixCopy)
        results.append(score)

    results = np.array(results)
    # Returns all the indeces with max scores
    filteredInxs = np.argwhere(results == np.amax(results))

    # Randomly selects from highest scored options
    final_choice = random.choice(filteredInxs)

    # Finally, places the chip in a chosen spot!
    self.parent.matrix[0][final_choice[0]].on_mouse_down(event)

# Drops a chip into a copied matrix
def simulateDrop(matrixCopy, colChoice):
    # Finds the valid row 
    for row in range(6-1, -1, -1):
        if matrixCopy[row][colChoice] == 0:
            break

    matrixCopy[row][colChoice] = 2
    return matrixCopy

# Calculates the score of a particular matrix from a perspective of a computer
def getScore(matrixCopy):
    num_threes = count_windows(matrixCopy, num_discs=3, mark=2, rows=6, columns=7)
    num_fours = count_windows(matrixCopy, num_discs=4, mark=2, rows=6, columns=7)
    # Number of thees for an opposing player
    num_threes_opp = count_windows(matrixCopy, num_discs=3, mark=1, rows=6, columns=7)

    # A formula, that calculates the total score for the particular play
    # If the drop results in a win, score will be super hight. 
    # If the drop results in a loss, score will be super low
    score = num_threes - 1e2*num_threes_opp + 1e6*num_fours
    return score

# Helper function for get_heuristic: counts number of windows satisfying specified heuristic conditions
# Basically calculates the number of specific combinations within a matrix
def count_windows(grid, num_discs, mark, rows, columns):
    num_windows = 0
    # horizontal
    for row in range(rows):
        for col in range(4):
            window = list(grid[row, col:col+4])
            if check_window(window, num_discs, mark):
                num_windows += 1

    # vertical
    for row in range(6-3):
        for col in range(7):
            window = list(grid[row:row+4, col])
            if check_window(window, num_discs, mark):
                num_windows += 1
    
    # positive diagonal
    for row in range(rows-(4-1)):
        for col in range(columns-(4-1)):
            window = list(grid[range(row, row+4), range(col, col+4)])
            if check_window(window, num_discs, mark):
                num_windows += 1

    # negative diagonal
    for row in range(4-1, rows):
        for col in range(columns-(4-1)):
            window = list(grid[range(row, row-4, -1), range(col, col+4)])
            if check_window(window, num_discs, mark):
                num_windows += 1

    return num_windows

# Helper function for get_heuristic: checks if window satisfies heuristic conditions
def check_window(window, num_discs, mark):
    return (window.count(mark) == num_discs and window.count(0) == 4-num_discs)