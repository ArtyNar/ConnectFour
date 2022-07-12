def computerTurn(event, self):
    print("Computer's turn!")
    self.parent.matrix[0][0].on_mouse_down(event)