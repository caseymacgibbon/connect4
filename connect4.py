import numpy as np
import random


class Board():
    def __init__(self):
        self.board = np.full((7,6), ".")
        self.players = ["X", "O"]
        self.turn = 0
        self.game_over = False
        self.moves = []
        
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
        gets the available moves and returns a string array of avail columns
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
        if len(self.getAvailableMoves()) ==0:
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
        """
        Returns the score of a move depending on whether or not there is an open space
        """
        score = 0
        r, c = row, col
        while 0 <= r < 7 and 0 <= c < 6 and self.board[r, c] != opponent:
            if self.board[r, c] == player:
                score += 1
            elif self.board[r, c] == ".":  
                score +=.5
            r += delta_row
            c += delta_col
        if score ==4:
            return 10000
        return score
    
def scoreMove(board, move):
    row = move - 1
    col = np.max(np.where(board.board[row] == "."))
    count = 0
    # counts how many tokens in each row
    for i in range(1,4):
        if col + i < 6 and board.board[row, col + i] == board.players[board.turn % 2]:
            count += 1
        if col - i >= 0 and board.board[row, col - i] == board.players[board.turn % 2]:
            count += 1
        if row + i < 7 and board.board[row + i, col] == board.players[board.turn % 2]:
            count += 1
        if row - i >= 0 and board.board[row - i, col] == board.players[board.turn % 2]:
            count += 1
    return count

def score_Move(board, move):
    row = move - 1
    col = np.max(np.where(board.board[row] == "."))
    player = board.players[board.turn % 2]
    opponent = board.players[(board.turn + 1) % 2]
    directions = [
            (1, 0),  # vertical
            (0, 1),  # horizontal
            (1, 1),  # diagonal +
            (1, -1)  # diagonal -
        ]
    for dr, dc in directions:
        # count number of player pieces forwards and backwards in the direction
        player_count = board.scoreDirection(row, col, dr, dc, player, opponent) + board.scoreDirection(row, col, -dr, -dc, player, opponent) - 1
        # count number of opponent pieces forwards and backwards in the direction
        #opponent_count = board.countDirection(row, col, dr, dc, opponent) + board.countDirection(row, col, -dr, -dc, opponent) - 1
        # multiply score by 10 (want a lot of consecutive pieces)
        score = player_count * 10
        # subtract opponents blocking
        #score = score - opponent_count
        #count+= score

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
    # random.shuffle(legalMoves)
    scores = []
    for move in legalMoves:
        # find the score of this move
        moveScore = scoreMove(board, move) * (depth + 1)/10
        # simulate doing the move
        board.move(move)
        # call the min function to find opponent's best move
        score = minMove(board, depth-1, moveScore)[1] + prevScore
        # undoes change
        board.undo()
        # compare scores of all possible next moves
        scores.append(score)
        if score > bestScore:
            bestScore = score
            bestMove = move
    return bestMove, bestScore, scores

def minMove(board, depth, prevScore):
   # base case
    if depth < 0 or board.game_over:
        return None, prevScore
    # else
    print("here")
    bestScore = float("inf")
    bestMove = None
    # shuffle all possible moves so it doesn't always do the same thing
    legalMoves = list(board.getAvailableMoves())
    # random.shuffle(legalMoves)
    for move in legalMoves:
        # find the score of this move and negate for the opponent
        moveScore = - scoreMove(board, move) * (depth + 1)/10
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
            move, score, scores = maxMove(board, 2, 0)
            print(scores)
            print("Best score: " + str(score))
            print("Computer's move: " + str(move))
            board.move(int(move))
            turn += 1
        elif turn % 2 == 1: # player's turn
            move = None # move not ever valid X
            while move not in board.getAvailableMoves(): # makes a list of strings instead of int
                move = input("Enter a valid move: ")
                if move.isnumeric():
                    move = int(move)
            board.move(move)
            turn += 1
        print(board)
    if turn % 2 == 0:
        print("You win!")
    elif turn % 2 == 1:
        print("You lost :(")

main()