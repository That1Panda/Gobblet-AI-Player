import pygame

import random
import time
import sys

from constants import GUIStyles

class GameBoard:
    """
    A class representing the game board.

    Attributes:
        GRID_SIZE (int): the size of the game board
        SQUARE_SIZE (int): the size of each square on the game board
        board (GameBoard): a 2D list representing the state of the game board
        WIDTH (int): the width of the game board
        HEIGHT (int): the height of the game board
        screen: the pygame screen object
        WHITE (tuple): RGB tuple representing the color white
        BLACK (tuple): RGB tuple representing the color black

    Methods:
        __init__(self, grid_size: int):
            Initializes the game board with the given grid size.

        draw_board(self):
            Draws the game board on the screen.

        check_win(self, player: str) -> bool:
            Checks if the specified player has won the game.

        evaluate_board(self) -> int or None:
            Evaluates the current state of the game board and returns the score.

        check_draw(self) -> bool:
            Checks if the game is a draw.
    """

    def __init__(self, grid_size: int):
        """
        Initializes the game board with the given grid size.

        Args:
            grid_size (int): the size of the game board
        """
        self.GRID_SIZE = grid_size
        self.SQUARE_SIZE = 400 // grid_size
        self.board = [[' ' for _ in range(grid_size)] for _ in range(grid_size)]
        self.WIDTH, self.HEIGHT = grid_size * self.SQUARE_SIZE, grid_size * self.SQUARE_SIZE
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Gobblet Game")
        self.WHITE = (255, 255, 255)
        self.screen.fill(GUIStyles.BACKGROUND_COLOR.value)

    def draw_board(self, player1, player2):
        """
        Draws the game board on the screen.

        Args:
            color1 (str): Color for player 1 ('W' or 'B')
            color2 (str): Color for player 2 ('W' or 'B')
        """
        self.screen.fill(GUIStyles.BACKGROUND_COLOR.value)


        # Draw the player1 stacks in the first column
        for i in range(3):
            for j in range (player1.stacks[i].__len__()):
                if(player1.stacks[i][j].is_EXT == True):
                    pygame.draw.circle(self.screen, (255, 0, 0),
                    center=(self.SQUARE_SIZE // 2,i * self.SQUARE_SIZE + self.SQUARE_SIZE // 2),
                    radius= player1.stacks[i][j].size * 6)
        # Draw the player2 stacks in the last column
        for i in range(3):
            for j in range (player2.stacks[i].__len__()):
                if(player2.stacks[i][j].is_EXT == True):
                    pygame.draw.circle(self.screen, (0, 0, 255),
                    center= (5 * self.SQUARE_SIZE + self.SQUARE_SIZE // 2,i * self.SQUARE_SIZE + self.SQUARE_SIZE // 2),
                    radius= player2.stacks[i][j].size * 6)

        # Draw the main game board
        for row in range(self.GRID_SIZE - 2):
            for col in range(1, self.GRID_SIZE - 1):  # Exclude the first and last columns
                pygame.draw.rect(self.screen, GUIStyles.BACKGROUND_COLOR.value,
                                 (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE), 0)
                pygame.draw.rect(self.screen, self.WHITE,
                                 (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE), 1)

                if len(self.board[row][col]) != 0:
                    piece = self.board[row][col]
                    if isinstance(self.board[row][col], list):
                        pygame.draw.circle(self.screen, (255, 10, 15)  if piece[-1].color == 'W' else (0, 0, 255),
                                        (col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2,
                                            row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2),
                                            radius= piece[-1].size * 6)


    def assign_initial_values(self, player1, player2):
        """
        Assigns initial values to the grids in the first and last columns.

        Args:
            player1 (Player): Player 1 object
            player2 (Player): Player 2 object
        """
        # Assign initial values in the first column and last columns
        for i in range(3):
            self.board[i][0] = player1.stacks[i]
            self.board[i][5] = player2.stacks[i]

        for i in range (0,4):
            for j in range(1,5):
                self.board[i][j] = []



    def check_win(self, player: str) -> bool:
        """
        Checks if the specified player has won the game.

        Args:
        player (str): a string representing the player ('X' or 'O')

        Returns:
        win (bool): True if the player has won, False otherwise.
        """
        for row in range(self.GRID_SIZE - 2):
            # Check if all elements in the row have the same symbol
            if all(self.board[row][col] and self.board[row][col][-1].symbol == player for col in range(1, self.GRID_SIZE - 1)):
                return True
            
        # Column check
        for col in range(1, self.GRID_SIZE - 1):
            if all(self.board[row][col] and self.board[row][col][-1].symbol == player for row in range(self.GRID_SIZE - 2)):
                return True

        # Diagonal checks
        if all(self.board[row][row+1] and self.board[row][row+1][-1].symbol == player for row in range(0, 4)) or all(
                self.board[row][4 - row] and self.board[row][4 - row][-1].symbol == player for row in range(0, 4)):
            return True

        return False

    def evaluate_board(self) -> int or None:
        """
        Evaluates the current state of the game board and returns the score.

        Returns:
            score (int | None): 1 if 'X' wins, -1 if 'O' wins, 0 for a draw, None if the game is ongoing.
        """
        if self.check_win('X'):
            return 1
        elif self.check_win('Y'):
            return -1
        elif self.check_draw():
            return 0

        return None

    def check_draw(self) -> bool:
        """
        Checks if the game is a draw.

        Returns:
            draw (bool): True if the game is a draw, False otherwise.
        """
        return all( len(self.board[row][col]) != 0 for row in range(self.GRID_SIZE-2) for col in range(1,self.GRID_SIZE-1))


# Example Usage:
#game_board = GameBoard(grid_size=4)

# time.sleep(5)
# pygame.quit()
# sys.exit()
