import pygame
import random
import time
import sys

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
        Initializes the game board with the given grid size and player entities.

        Args:
            grid_size (int): the size of the game board
            player_entities (List[List[int]]): list of player entities with initial circle sizes
        """
        self.GRID_SIZE = grid_size
        self.SQUARE_SIZE = 400 // grid_size
        self.EXTRA_SPACE = 2
        self.stacks=3
        self.entities=4
        self.entity_size=15
        self.player_entities = [[4, 1, 2], [3, 4, 2]]
        self.board = [[' ' for _ in range(grid_size)] for _ in range(grid_size)]
        self.WIDTH = (grid_size + 2 * self.EXTRA_SPACE) * self.SQUARE_SIZE
        self.HEIGHT = grid_size * self.SQUARE_SIZE
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Gobblet Game")
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

    def draw_main_grid(self):
        """
        Draw the main 4x4 grid on the screen.
        """
        for row in range(self.GRID_SIZE):
            for col in range(self.EXTRA_SPACE, self.GRID_SIZE + self.EXTRA_SPACE):
                pygame.draw.rect(self.screen, self.BLACK,
                                 (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE), 0)
                pygame.draw.rect(self.screen, self.WHITE,
                                 (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE), 1)

                if self.board[row][col - self.EXTRA_SPACE] != ' ':
                    piece = self.board[row][col - self.EXTRA_SPACE]
                    pygame.draw.circle(self.screen, (255, 0, 0) if piece == 'X' else (0, 0, 255),
                                       ((col - self.EXTRA_SPACE) * self.SQUARE_SIZE + self.SQUARE_SIZE // 2,
                                        row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2),
                                       self.SQUARE_SIZE // 3)

    def draw_extra_columns(self):
        """
        Draw the extra columns on the left and right sides.
        """
        for row in range(self.stacks):
            
                x_left =0
                y_left = row * int((self.SQUARE_SIZE * 4) / self.stacks)
                pygame.draw.rect(self.screen, self.BLACK, (x_left, y_left, self.SQUARE_SIZE * 2, int((self.SQUARE_SIZE * 4) / self.stacks)), 0)
                pygame.draw.rect(self.screen, self.WHITE, (x_left, y_left, self.SQUARE_SIZE * 2, int((self.SQUARE_SIZE * 4) / self.stacks)), 1)

                x_right = self.SQUARE_SIZE * 6
                y_right = row * int((self.SQUARE_SIZE * 4) / self.stacks)
                pygame.draw.rect(self.screen, self.BLACK, (x_right, y_right, self.SQUARE_SIZE * 2, int((self.SQUARE_SIZE * 4) / self.stacks)), 0)
                pygame.draw.rect(self.screen, self.WHITE, (x_right, y_right, self.SQUARE_SIZE * 2, int((self.SQUARE_SIZE * 4) / self.stacks)), 1)

    def draw_circles(self):
        """
        Draw circles on the screen based on player entities.
        """
        for row in range(self.stacks):
            
                # Draw left side circles and make them dependent on player entities number (the bigger number the bigger circle)
                x_left = self.SQUARE_SIZE 
                y_left = row * int((self.SQUARE_SIZE * 4) / self.stacks) + int((self.SQUARE_SIZE * 4) / self.stacks)/2
                pygame.draw.circle(self.screen, (255, 0, 0), (x_left, y_left), self.player_entities[0][row]*self.entity_size)

                # Draw right side circles and make them dependent on player entities number (the bigger number the bigger circle)
                x_right = self.SQUARE_SIZE * 6 + self.SQUARE_SIZE
                y_right = row * int((self.SQUARE_SIZE * 4) / self.stacks)  + int((self.SQUARE_SIZE * 4) / self.stacks)/2
                pygame.draw.circle(self.screen, (0, 0, 255), (x_right, y_right), self.player_entities[1][row]*self.entity_size)




    def draw_board(self):
        """
        Draws the game board on the screen.
        """
        self.screen.fill(self.BLACK)
        self.draw_main_grid()
        self.draw_extra_columns()
        self.draw_circles()
        pygame.display.flip()

    def check_win(self, player: str) -> bool:
        """
        Checks if the specified player has won the game.

        Args:
            player (str): a string representing the player ('X' or 'O')

        Returns:
            win (bool): True if the player has won, False otherwise.
        """
        for row in range(self.GRID_SIZE):
            if all(self.board[row][col] == player for col in range(self.GRID_SIZE)):
                return True

        for col in range(self.GRID_SIZE):
            if all(self.board[row][col] == player for row in range(self.GRID_SIZE)):
                return True

        if all(self.board[i][i] == player for i in range(self.GRID_SIZE)) or all(
                self.board[i][self.GRID_SIZE - i - 1] == player for i in range(self.GRID_SIZE)):
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
        elif self.check_win('O'):
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
        return all(self.board[row][col] != ' ' for row in range(self.GRID_SIZE) for col in range(self.GRID_SIZE))


# Example Usage:
game_board = GameBoard(grid_size=4)
game_board.draw_board()
time.sleep(5)
pygame.quit()
sys.exit()
