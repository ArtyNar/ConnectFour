###
# Even better - looks N steps ahead into a future!
# I will use a minimax algorithm to help the agent look farther into the future and make better-informed decisions.
###

import numpy as np
import random 
import copy

# How deep to make the game tree: higher values take longer to run!
N_STEPS = 3

class Config:
    columns = 7
    rows = 6
    inarow = 4

def nstepAgent(event, parent, mark):
    # Get list of valid moves
    valid_moves = [col for col in range(7) if parent.matrix[0][col].isFilled() == False]

     # Check if the game is over
    if(len(valid_moves) == 0):
        parent.isTie = True
        parent.scores[2] += 1
        parent.resetAll()
        return

    config = Config()

    matrixCopy = np.asarray(copy.deepcopy(parent.decodedMatrix))

    # Use the heuristic to assign a score to each possible board in the next step
    scores = dict(zip(valid_moves, [score_move(matrixCopy, col, mark+1, config, N_STEPS) for col in valid_moves]))

    print(scores)
    # Get a list of columns (moves) that maximize the heuristic
    max_cols = [key for key in scores.keys() if scores[key] == max(scores.values())]
    # Select at random from the maximizing columns

    parent.matrix[0][random.choice(max_cols)].on_mouse_down(event)

# Calculates the score of a particular matrix from a perspective of a computer
# Only looks at number of threes and fours on a board. Works, but can be better
def nStepHeuristic(matrixCopy, mark, config):
    num_threes = count_windows(matrixCopy, 3, mark, config)
    num_fours = count_windows(matrixCopy, 4, mark, config)
    num_threes_opp = count_windows(matrixCopy, 3, mark%2+1, config)
    num_fours_opp = count_windows(matrixCopy, 4, mark%2+1, config)
    score = num_threes - 1e2*num_threes_opp - 1e4*num_fours_opp + 1e6*num_fours
    return score


# Uses minimax to calculate value of dropping piece in selected column
def score_move(grid, col, mark, config, nsteps):
    next_grid = simulateDrop(grid, col, mark, config)
    score = minimax(next_grid, nsteps-1, False, mark, config)
    return score

##
#
# minimax algorithm: the agent chooses moves to get a score that is as high as possible, 
# and it assumes the opponent will counteract this by choosing moves to force the score to be as low as possible.
#
##
def minimax(node, depth, maximizingPlayer, mark, config):
    is_terminal = is_terminal_node(node, config)
    valid_moves = [c for c in range(config.columns) if node[0][c] == 0]
    if depth == 0 or is_terminal:
        return nStepHeuristic(node, mark, config)
    if maximizingPlayer:
        value = -np.Inf
        for col in valid_moves:
            child = simulateDrop(node, col, mark, config)
            value = max(value, minimax(child, depth-1, False, mark, config))
        return value
    else:
        value = np.Inf
        for col in valid_moves:
            child = simulateDrop(node, col, mark%2+1, config)
            value = min(value, minimax(child, depth-1, True, mark, config))
        return value


# Helper function for minimax: checks if agent or opponent has four in a row in the window
def is_terminal_window(window, config):
    return window.count(1) == config.inarow or window.count(2) == config.inarow

# Helper function for minimax: checks if game has ended
def is_terminal_node(grid, config):
    # Check for draw 
    if list(grid[0, :]).count(0) == 0:
        return True
    # Check for win: horizontal, vertical, or diagonal
    # horizontal 
    for row in range(config.rows):
        for col in range(config.columns-(config.inarow-1)):
            window = list(grid[row, col:col+config.inarow])
            if is_terminal_window(window, config):
                return True
    # vertical
    for row in range(config.rows-(config.inarow-1)):
        for col in range(config.columns):
            window = list(grid[row:row+config.inarow, col])
            if is_terminal_window(window, config):
                return True
    # positive diagonal
    for row in range(config.rows-(config.inarow-1)):
        for col in range(config.columns-(config.inarow-1)):
            window = list(grid[range(row, row+config.inarow), range(col, col+config.inarow)])
            if is_terminal_window(window, config):
                return True
    # negative diagonal
    for row in range(config.inarow-1, config.rows):
        for col in range(config.columns-(config.inarow-1)):
            window = list(grid[range(row, row-config.inarow, -1), range(col, col+config.inarow)])
            if is_terminal_window(window, config):
                return True
    return False

def simulateDrop(grid, col, mark, config):
    next_grid = grid.copy()
    for row in range(config.rows-1, -1, -1):
        if next_grid[row][col] == 0:
            break
    next_grid[row][col] = mark
    return next_grid

# Helper function for get_heuristic: counts number of windows satisfying specified heuristic conditions
def count_windows(grid, num_discs, piece, config):
    num_windows = 0
    # horizontal
    for row in range(config.rows):
        for col in range(config.columns-(config.inarow-1)):
            window = list(grid[row, col:col+config.inarow])
            if check_window(window, num_discs, piece, config):
                num_windows += 1
    # vertical
    for row in range(config.rows-(config.inarow-1)):
        for col in range(config.columns):
            window = list(grid[row:row+config.inarow, col])
            if check_window(window, num_discs, piece, config):
                num_windows += 1
    # positive diagonal
    for row in range(config.rows-(config.inarow-1)):
        for col in range(config.columns-(config.inarow-1)):
            window = list(grid[range(row, row+config.inarow), range(col, col+config.inarow)])
            if check_window(window, num_discs, piece, config):
                num_windows += 1
    # negative diagonal
    for row in range(config.inarow-1, config.rows):
        for col in range(config.columns-(config.inarow-1)):
            window = list(grid[range(row, row-config.inarow, -1), range(col, col+config.inarow)])
            if check_window(window, num_discs, piece, config):
                num_windows += 1
    return num_windows

def check_window(window, num_discs, mark, config):
    return (window.count(mark) == num_discs and window.count(0) == 4-num_discs)