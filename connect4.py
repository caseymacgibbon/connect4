import numpy as np
import random


class Board():
    def __init__(self):
        self.board = np.full((7,6), ".")
        self.players = ["X", "O"]
        self.turn = 0
        self.game_over = False
        
    def __str__(self): # makes board print nicely
        p = "1 2 3 4 5 6 7"
        for col in range(np.shape(self.board)[1]):
            p += "\n"
            for row in range(np.shape(self.board)[0]):
                p += (self.board[row, col])
                p += " "
        return p
    
    def move(self, row): # adds a piece at the specified column
        col = np.max(np.where(self.board[row - 1] == "."))
        self.board[row - 1, col] = self.players[self.turn % 2]
        self.turn += 1
        self.game_over = self.checkWinner(row - 1, col) != None and self.checkFull()

    def checkWinner(self, row, col): # checks if the most recent move makes a sequence of 4
        char = self.board[row, col]
        # check vertical
        count = 0
        shift = 0
        while col + shift < 6 and self.board[row, col + shift] == char:
            count += 1
            shift += 1
        shift = 1
        while col - shift >= 0 and self.board[row, col - shift] == char:
            count += 1
            shift +=1
        if count >= 4:
            return char
        # check horizontal
        count = 0
        shift = 0
        while row + shift < 7 and self.board[row + shift, col] == char:
            count += 1
            shift += 1
        shift = 1
        while row - shift >= 0 and self.board[row - shift, col] == char:
            count += 1
            shift +=1
        if count >= 4:
            return char
        # check positive diagonal
        count = 0
        shift = 0
        while row + shift < 7 and col + shift < 6 and self.board[row + shift, col + shift] == char:
            count += 1
            shift += 1
        shift = 1
        while row - shift >= 0 and col - shift >= 0 and self.board[row - shift, col - shift] == char:
            count += 1
            shift +=1
        if count >= 4:
            return char
        # check negative diagonal
        count = 0
        shift = 0
        while row + shift < 7 and col - shift >= 0 and self.board[row + shift, col - shift] == char:
            count += 1
            shift += 1
        shift = 1
        while row - shift >= 0 and col + shift < 6 and self.board[row - shift, col + shift] == char:
            count += 1
            shift +=1
        if count >= 4:
            return char
        return None
    
    def getAvailableMoves(self):
        avail_moves = []
        for col in range(7):
            # Check if there's room in the column
            if "." in self.board[col]:
                avail_moves.append(str(col+1))  
        return avail_moves
        
    def checkFull(self):
        if self.getAvailableMoves() is None:
            return False
        return False
def main():
    board = Board()
    # figure out who is going first (X always goes first)
    comp = None
    while comp not in ["X", "O"]:
        comp = input("Is the computer X or O? ")
    if comp == "X":
        turn = 0
    elif comp == "O":
        turn = 1
    # play the game
    print(board)
    while not board.game_over:
        if turn % 2 == 0: # computer's turn
            avail_moves = board.getAvailableMoves()
            print(avail_moves)
            move = random.choice(avail_moves)
            print("Computer's move: " + str(move))
            board.move(int(move))
            turn += 1
        elif turn % 2 == 1: # player's turn
            move = None # move not ever valid X
            while move not in board.getAvailableMoves(): # makes a list of strings instead of int
                print(board.getAvailableMoves())
                move = input("Enter a valid move: ")
            board.move(int(move))
            turn += 1
        print(board)
    if turn % 2 == 0:
        print("You win!")
    elif turn % 2 == 1:
        print("You lost :(")

main()