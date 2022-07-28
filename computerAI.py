import random 
import copy
import numpy as np


# Mindless random agent, plots the chips randomly
def randomAgent(event, parent):
    valid_moves = [col for col in range(7) if parent.matrix[0][col].isFilled() == False]
    choiceCol = random.choice(valid_moves)

    parent.matrix[0][choiceCol].on_mouse_down(event)

###
# A better agent, looking one step ahead
# One-step lookahead agent will:
# - use the heuristic to assign a score to each possible valid move, and
# - select the move that gets the highest score. (If multiple moves get the high score, we select one at random.)
###
def oneStepAgent(event, parent):
    # "Simply" chooses a valid move
    valid_moves = [col for col in range(7) if parent.matrix[0][col].isFilled() == False]

    # Check if the game is over
    if(len(valid_moves) == 0):
        parent.isTie = True
        parent.scores[2] += 1
        parent.resetAll()
        return

    # Iterates over each potential chip drop, gets the score and stores all of them in an array
    results = []
    for col in valid_moves:
        # Makes a copy of a matrix to simulate
        matrixCopy = np.asarray(copy.deepcopy(parent.decodedMatrix))
        # Drops a piece into a copy
        matrixCopy = simulateDrop(matrixCopy, col)

        # Here, I can change which heuristic function I get to use
        score = oneStepGetScoreV2(matrixCopy)
        results.append(score)

    results = np.array(results)
    # Returns all the indeces with max scores
    filteredInxs = np.argwhere(results == np.amax(results))

    # Randomly selects from highest scored options
    final_choice = random.choice(filteredInxs)

    # Finally, places the chip in a chosen spot!
    parent.matrix[0][valid_moves[final_choice[0]]].on_mouse_down(event)

###
# Even better - looks N steps ahead into a future!
# I will use a minimax algorithm to help the agent look farther into the future and make better-informed decisions.
#
#
###
def nStepAgent(event, self):
    print("nstep")
    
# Drops a chip into a copied matrix
def simulateDrop(matrixCopy, colChoice):
    # Finds the valid row 
    for row in range(6-1, -1, -1):
        if matrixCopy[row][colChoice] == 0:
            break

    matrixCopy[row][colChoice] = 2
    return matrixCopy

# Calculates the score of a particular matrix from a perspective of a computer
# Only looks at number of threes and fours on a board. Works, but can be better
def oneStepGetScore(matrixCopy):
    # This are the values for our heuristics
    A = 1e2
    B = 1e6

    num_threes = count_windows(matrixCopy, num_discs=3, mark=2, rows=6, columns=7)
    num_fours = count_windows(matrixCopy, num_discs=4, mark=2, rows=6, columns=7)
    # Number of thees for an opposing player
    num_threes_opp = count_windows(matrixCopy, num_discs=3, mark=1, rows=6, columns=7)

    # A formula, that calculates the total score for the particular play
    # If the drop results in a win, score will be super hight. 
    # If the drop results in a loss, score will be super low
    score = num_threes - A*num_threes_opp + B*num_fours
    return score

# Uses a better heuristics function, accounting for how many twos there are 
# for each player
def oneStepGetScoreV2(matrixCopy):
    # This are the values for our heuristiscs
    A = 1000000
    B = 5
    C = 2
    D = -2
    E = -30
    
    num_twos = count_windows(matrixCopy, num_discs=2, mark=2, rows=6, columns=7)
    num_threes = count_windows(matrixCopy, num_discs=3, mark=2, rows=6, columns=7)
    num_fours = count_windows(matrixCopy, num_discs=4, mark=2, rows=6, columns=7)
    num_twos_opp = count_windows(matrixCopy, num_discs=2, mark=1, rows=6, columns=7)
    num_threes_opp = count_windows(matrixCopy, num_discs=3, mark=1, rows=6, columns=7)

    score = A*num_fours + B*num_threes + C*num_twos + D*num_twos_opp + E*num_threes_opp
    return score

# Helper function for get_heuristic: counts number of windows satisfying specified heuristic conditions
# Basically calculates the number of specific combinations within a matrix
def count_windows(grid, num_discs, mark, rows, columns):
    num_windows = 0
    # horizontal
    for row in range(rows):
        # 4 windows to check in a row
        for col in range(4):
            window = list(grid[row, col:col+4])
            if check_window(window, num_discs, mark):
                num_windows += 1

    # vertical
    # 3 windows to check in a col
    for row in range(3):
        for col in range(columns):
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
# Checks if the window has asked amount of disks in it and empty spaces
def check_window(window, num_discs, mark):
    return (window.count(mark) == num_discs and window.count(0) == 4-num_discs)