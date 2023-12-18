import pygame
import random
import time
from gameBoard import GameBoard
from Alpha_Beta_Final import AIAlgorithms


class GobbletNode:
    """
    A class representing a GobbletNode.

    Attributes:
        size (int): the size of the gobblet
        color (str): the color of the gobblet ('X' or 'O')

    Methods:
        __init__(self, size: int, color: str):
            Initializes the GobbletNode with the specified size and color.
    """
    def __init__(self, size: int, color: str, symbol: str, row, col, is_EXT: bool = False):
        self.size = size
        self.color = color
        self.symbol = symbol
        self.is_EXT = is_EXT
        self.row = row
        self.col = col


class Player:
    """
    A class representing a player in the game.
    ... (rest of the class definition remains unchanged)
    """
    players = []  # Class variable to keep track of all players

    def __init__(self, player_type: str, symbol: str, color: str, algo: str = None):
        """
        Initializes the Player with the specified player type, symbol, and algorithm.

        Args:
            player_type (str): the type of player ('human' or 'computer')
            symbol (str): the symbol representing the player ('X' or 'O')
            algo (str): the algorithm used for the computer player ('random', 'minimax', or 'alpha_beta_pruning')
        """
        self.player_type = player_type
        self.symbol = symbol
        self.algo = algo
        self.color = color

        # Automatically set col based on player order
        if len(Player.players) % 2 != 0:
            col = 5
        else:
            col = 0

        self.stacks = [
            [GobbletNode(1, color, symbol, row=0, col=col), GobbletNode(2, color, symbol,row=0, col=col), GobbletNode(3, color, symbol,row=0, col=col), GobbletNode(4, color, symbol,row=0, col=col, is_EXT=True)],
            [GobbletNode(1, color, symbol, row=1, col=col), GobbletNode(2, color, symbol,row=1, col=col), GobbletNode(3, color, symbol, row=1, col=col), GobbletNode(4, color,  symbol,row=1, col=col, is_EXT=True)],
            [GobbletNode(1, color, symbol, row=2, col=col), GobbletNode(2, color, symbol, row=2, col=col), GobbletNode(3, color, symbol, row=2, col= col), GobbletNode(4, color,  symbol, row=2, col=col,is_EXT=True)]
        ]

        # Add the player to the players list
        Player.players.append(self)


    def make_move(self, board: GameBoard) -> tuple or None:
        """
        Makes a move based on the player type.

        Args:
            board (GameBoard): the game board

        Returns:
            move (tuple or None): the coordinates of the move (row, column)
        """
        if self.player_type == 'human':
            return self.human_move(board)
        elif self.player_type == 'computer':
            return self.computer_move(board)
        else:
            raise ValueError("Invalid player type")
        


    def human_move(self, board: GameBoard) -> tuple:
        """
        Allows a human player to make a move by clicking on the game board.

        Args:
            board (GameBoard): the game board

        Returns:
            clicked_row, clicked_col (tuple): the coordinates of the clicked position
        """
        selected_row , selected_col = self.human_select(board)
        print(selected_row , selected_col)
        move_made = False

        while not move_made:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX, mouseY = pygame.mouse.get_pos()
                    clicked_row, clicked_col = mouseY // board.SQUARE_SIZE, mouseX // board.SQUARE_SIZE
                    #print(board.board[clicked_row][clicked_col][-1].size,board.board[clicked_row][clicked_col][-1].is_EXT)
                    if clicked_row == selected_row and clicked_col == selected_col:
                        print("you make unselection please select again")
                        return False 
                    if clicked_row in range(0, 4) and (clicked_col == 0 or clicked_col == 5):
                        print("Please select any rect in the board")
                        continue
                    
                    if clicked_row in range (0,4) and clicked_col in range (1,4):
                        if selected_row in range(0,3) and (selected_col == 0 or selected_col == 5):
                            if len(board.board[clicked_row][clicked_col]) == 0:
                                board.board[clicked_row][clicked_col].append(self.stacks[selected_row].pop())

                                if len(self.stacks[selected_row]) !=0:
                                    self.stacks[selected_row][-1].is_EXT = True
                                move_made = True
                                return clicked_row, clicked_col
                            else :
                                if board.board[clicked_row][clicked_col][-1].size < self.stacks[selected_row][-1].size:
                                    board.board[clicked_row][clicked_col].append(self.stacks[selected_row].pop())
                                    move_made = True
                                else :
                                    print("transaction can not be done")

                        elif selected_row in range(0,4) and (selected_col in range (1,5)):
                            if len(board.board[clicked_row][clicked_col]) == 0:
                                board.board[clicked_row][clicked_col].append(board.board[selected_row][selected_col].pop())
                                move_made = True
                            else:
                                if board.board[clicked_row][clicked_col][-1].size < board.board[selected_row][selected_col][-1].size:
                                    board.board[clicked_row][clicked_col].append(board.board[selected_row][selected_col].pop())
                                    move_made = True
                                else :
                                    print("transaction can not be done")


    def human_select(self,board: GameBoard) -> tuple:
        clicked_row = 0  
        clicked_col = 0
        selected = False
        while not selected:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX, mouseY = pygame.mouse.get_pos()
                    clicked_row, clicked_col = mouseY // board.SQUARE_SIZE, mouseX // board.SQUARE_SIZE
                    #print(board.board[clicked_row][clicked_col][-1].size,board.board[clicked_row][clicked_col][-1].is_EXT)
                    if len (board.board[clicked_row][clicked_col]) == 0:
                        print("please select a suitable node")
                        continue
                    elif clicked_row in range (0,4) and clicked_col in range (0,6):
                        if board.board[clicked_row][clicked_col][-1].symbol == self.symbol :
                            selected = True
                        else :
                            print("please select from your nodes ")
                            continue
        return clicked_row, clicked_col

    def computer_move(self, board: GameBoard) -> tuple or None:
        """
        Makes a move for a computer player based on the selected algorithm.

        Args:
            board (GameBoard): the game board

        Returns:
            move (tuple or None): the coordinates of the move (row, column)
        """
        if self.algo == 'random':
            return self.random_move(board)
        
        elif self.algo == 'alpha_beta_pruning':
            return self.alpha_beta_pruning_move(board)
        else:
            raise ValueError("Invalid algorithm")

    # def random_move(self, board: GameBoard) -> tuple or None:
    #     """
    #     Makes a random move for the computer player.

    #     Args:
    #         board (GameBoard): the game board

    #     Returns:
    #         random_move (tuple or None): the coordinates of the randomly chosen move (row, column)
    #     """
    #     empty_cells = [(row, col) for row in range(board.GRID_SIZE) for col in range(board.GRID_SIZE) if
    #     board.board[row][col] == ' ']
    #     if empty_cells:
    #         row, col = random.choice(empty_cells)
    #         board.board[row][col] = self.symbol
    #         return row, col
    #     else:
    #         return None

    def alpha_beta_pruning_move(self, board: GameBoard) -> tuple or None:
        """
        
        Makes a move for the computer player using the Alpha-Beta Pruning algorithm.

        Args:
            board (GameBoard): the game board

        Returns:
            best_move (tuple or None): the coordinates of the best move (row, column)
        
        """
        AI = AIAlgorithms
        score , nextboard ,best_move = AIAlgorithms.get_best_move(AI,board,False, 'Y', 3, 5)
        #row, col = best_move
        board.board[best_move.newRow][best_move.newCol].append(board.board[best_move.curRow][best_move.curCol].pop())
        return best_move


# Example Usage:
# move = player1.make_move(board)
# board.draw_board()
# move = player2.make_move(board)
# board.draw_board()
# time.sleep(2)
