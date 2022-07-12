###
#
#   The next set of functions is used to 
#   calculate the score after each turn of the game.
#   We have to check score horizontally, vertically, and diagonally.
#
###
def setScore(self, playerNum):
    horiz = checkRight(self, playerNum) + checkLeft(self, playerNum) - 1
    vert = checkDown(self, playerNum) 
    diag = checkDiagonal(self, playerNum)
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