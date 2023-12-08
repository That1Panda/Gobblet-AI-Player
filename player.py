import pygame
import random
import time
from gameBoard import GameBoard

class Player:
    def __init__(self, player_type, symbol, algo=None):
        self.player_type = player_type  # 'human' or 'computer'
        self.symbol = symbol  # 'X' or 'O'
        self.algo = algo  # Algorithm used for the computer player (if applicable)

    def make_move(self, board):
        if self.player_type == 'human':
            return self.human_move(board)
        elif self.player_type == 'computer':
            return self.computer_move(board)
        else:
            raise ValueError("Invalid player type")

    def human_move(self, board):
        move_made = False

        while not move_made:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX, mouseY = pygame.mouse.get_pos()
                    clicked_row, clicked_col = mouseY // board.SQUARE_SIZE, mouseX // board.SQUARE_SIZE

                    if board.board[clicked_row][clicked_col] == ' ':
                        board.board[clicked_row][clicked_col] = self.symbol
                        move_made = True
                        
                        return clicked_row, clicked_col

    def computer_move(self, board):
        if self.algo == 'random':
            row,column= self.random_move(board)
            board.board[row][column]=self.symbol
            return row,column

        elif self.algo == 'minimax':
            return self.minimax_move(board)
        else:
            raise ValueError("Invalid algorithm")

    def random_move(self, board):
        empty_cells = [(row, col) for row in range(board.GRID_SIZE) for col in range(board.GRID_SIZE) if
                       board.board[row][col] == ' ']
        if empty_cells:
            return random.choice(empty_cells)
        else:
            return None

    def minimax_move(self, board):
        """Not correct yet"""
        best_score = float('-inf')
        best_move = None

        for move in [(row, col) for row in range(board.GRID_SIZE) for col in range(board.GRID_SIZE) if
                     board.board[row][col] == ' ']:
            row, col = move
            board.board[row][col] = self.symbol
            score = board.evaluate_board()
            board.board[row][col] = ' '  # Undo the move

            if score > best_score:
                best_score = score
                best_move = move

        return best_move

# Example Usage:
# player1 = Player(player_type='human', symbol='X')
# player2 = Player(player_type='computer', symbol='O', algo='random')
# board = GameBoard(grid_size=4)
# board.draw_board()
# move = player1.make_move(board)
# board.draw_board()
# move = player2.make_move(board)
# board.draw_board()
# time.sleep(4)
