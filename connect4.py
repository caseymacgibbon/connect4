import numpy as np
import random

class Board():
    '''
    board framework for playing Connect 4
    '''
    def __init__(self):
        self.board = np.full((7,6), ".") # size of board and symbol for empty space
        self.players = ["X", "O"] # symbols used on the board
        self.turn = 0 # even/odd determines whose turn it is
        self.game_over = False # True if one of the players has 4 in a row
        self.moves = [] # tracks past moves, allowing for undo
        
    def __str__(self): 
        """
        makes board print nicely
        """
        p = "1 2 3 4 5 6 7"
        for col in range(np.shape(self.board)[1]):
            p += "\n"
            for row in range(np.shape(self.board)[0]):
                p += (self.board[row, col])
                p += " "
        return p
    
    def move(self, row):
        """
        adds a piece at the specified column
        """
        col = np.max(np.where(self.board[row - 1] == "."))
        self.board[row - 1, col] = self.players[self.turn % 2]
        self.turn += 1
        self.game_over = self.checkWinner(row - 1, col) != None or self.checkFull()
        self.moves.append(row - 1)

    def undo(self):
        """
        undoes the most recent move
        """
        row = self.moves[-1]
        col = np.min(np.where(self.board[row] != "."))
        self.board[row, col] = "."
        self.moves.pop(-1)
        self.turn -= 1

    def checkWinner(self, row, col): 
        """
        Checks if the most recent move makes a sequence of 4 in any direction.
        """
        directions = [
            (1, 0),  # vertical
            (0, 1),  # horizontal
            (1, 1),  # diagonal +
            (1, -1)  # diagonal -
        ]

        for dr, dc in directions:
            # for every direction, count forwards and backwards
            # dr and dc are pos for first and neg for second
            # take out -1 because row, col counted twice
            if self.countDirection(row, col, dr, dc, self.board[row, col]) + self.countDirection(row, col, -dr, -dc, self.board[row, col]) - 1 >= 4:
                return self.board[row, col]
        return None
    
    def getAvailableMoves(self):
        """
        gets the available moves and returns a string array of available columns
        """
        avail_moves = []
        for col in range(7):
            # Check if there's room in the column
            if "." in self.board[col]:
                avail_moves.append(col+1)
        return avail_moves
        
    def checkFull(self):
        """
        Checks if the board is full
        """
        if len(self.getAvailableMoves()) == 0:
            return True
        return False
    
    def countDirection(self, row, col, delta_row, delta_col, player):
        """
        Count the number of consecutive pieces in a given direction.
        """
        count = 0
        r, c = row, col
        while 0 <= r < 7 and 0 <= c < 6 and self.board[r, c] == player:
            count += 1
            r += delta_row
            c += delta_col
        return count
    
    def scoreDirection(self, row, col, delta_row, delta_col, player, opponent):
        '''
        Returns the score based on tokens in one direction (horizontal, vertical, positive/negative diagonal)
        '''
        score = 0
        # forwards
        r, c = row, col
        r += delta_row
        c += delta_col
        counter = 0
        while 0 <= r < 7 and 0 <= c < 6 and self.board[r, c] != opponent and abs(row - r) < 4 and abs(row - r) < 4:
            if self.board[r, c] == player:
                score += 1 + counter / 10 # increase for more in the same direction, ie. getting 3 in a row is better than getting 2 in a row twice
            r += delta_row
            c += delta_col
            counter += 1
        # backwards
        r, c = row, col
        r -= delta_row
        c -= delta_col
        while 0 <= r < 7 and 0 <= c < 6 and self.board[r, c] != opponent and abs(row - r) < 4 and abs(row - r) < 4:
            if self.board[r, c] == player:
                score += 1 + counter / 10 # increase for more in the same direction
            r -= delta_row
            c -= delta_col
            counter += 1
        if score >= 3: # hugely incentivize winning
            score = 1000
        return score

    def scoreMove(self, move):
        """
            Returns the score of a move depending on where other tokens/empty space are
        """
        row = move - 1
        col = np.max(np.where(self.board[row] == "."))
        player = self.players[self.turn % 2]
        opponent = self.players[(self.turn + 1) % 2]
        directions = [
                (1, 0),  # vertical
                (0, 1), # horizontal
                (1, 1),  # diagonal +
                (1, -1)  # diagonal -
            ]
        score = 0
        for dr, dc in directions:
            # count number of player pieces in the direction
            player_count = self.scoreDirection(row, col, dr, dc, player, opponent)
            score += player_count
        return score

    
def maxMove(board, depth, prevScore):
    # base case
    if depth < 0 or board.game_over:
        return None, prevScore
    # else
    # set low best score
    bestScore = float("-inf")
    bestMove = None
    # shuffle all possible moves so it doesn't always do the same thing
    legalMoves = list(board.getAvailableMoves())
    random.shuffle(legalMoves)
    for move in legalMoves:
        # find the score of this move, multiply by depth to add urgency
        moveScore = board.scoreMove(move) * depth / 10
        # simulate doing the move
        board.move(move)
        # call the min function to find opponent's best move
        score = minMove(board, depth-1, moveScore)[1] + prevScore
        # undoes change
        board.undo()
        # compare scores of all possible next moves
        if score > bestScore:
            bestScore = score
            bestMove = move
    return bestMove, bestScore

def minMove(board, depth, prevScore):
   # base case
    if depth < 0 or board.game_over:
        return None, prevScore
    # else
    bestScore = float("inf")
    bestMove = None
    # shuffle all possible moves so it doesn't always do the same thing
    legalMoves = list(board.getAvailableMoves())
    random.shuffle(legalMoves)
    for move in legalMoves:
        # find the score of this move and negate for the opponent, multiply by depth to add urgency
        moveScore = - board.scoreMove(move) * depth / 10
        # simulate doing the move
        board.move(move)
        # call the max function to find computers's best move
        score = maxMove(board, depth-1, moveScore)[1] + prevScore
        # undoes change
        board.undo()
        # compare scores of all possible next moves
        if score < bestScore:
            bestScore = score
            bestMove = move
    return bestMove, bestScore
    
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
            depth = 5
            move, score = maxMove(board, depth - 1, 0)
            print("Best score: " + str(score))
            print("Computer's move: " + str(move))
            board.move(int(move))
            turn += 1
        elif turn % 2 == 1: # player's turn
            move = None # reset move
            while move not in board.getAvailableMoves(): # makes a list of strings instead of int
                move = input("Enter a valid move: ")
                if move.isnumeric():
                    move = int(move)
            board.move(move)
            turn += 1
        print(board)
    if board.checkFull() == True:
        print("Tie.")
    elif turn % 2 == 0:
        print("You win!")
    elif turn % 2 == 1:
        print("You lost :(")

main()