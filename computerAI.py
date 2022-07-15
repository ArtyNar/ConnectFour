
import random 

# Mindless random agent, plots the chips randomly
def randomAgent(event, self):
    print("Random")

    valid_moves = [col for col in range(7) if self.parent.matrix[0][col].isFilled() == False]
    choiceCol = random.choice(valid_moves)

    self.parent.matrix[0][choiceCol].on_mouse_down(event)


def betterAgent(event, self):
    print("Computer's turn!")

    # "Simply" chooses a valid move
    valid_moves = [col for col in range(7) if self.parent.matrix[0][col].isFilled() == False]
    # print(valid_moves)

    matrixCopy = self.parent.decodedMatrix



    choiceCol = random.choice(valid_moves)
    
    matrixCopy = simulateDrop(matrixCopy, choiceCol)
    score = getScore(matrixCopy)

    #self.parent.matrix[0][choiceCol].on_mouse_down(event)

def simulateDrop(matrixCopy, colChoice):
    score = 0

    for row in range(6-1, -1, -1):
        if matrixCopy[row][colChoice] == 0:
            break

    matrixCopy[row][colChoice] = 5
    return matrixCopy

def getScore(matrixCopy):
    score = 0
    return score