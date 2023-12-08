import pygame
import random
import time
import sys

class GameBoard:
    def __init__(self, grid_size):
        self.GRID_SIZE = grid_size
        self.SQUARE_SIZE = 400 // grid_size
        self.board = [[' ' for _ in range(grid_size)] for _ in range(grid_size)]
        self.WIDTH, self.HEIGHT = grid_size * self.SQUARE_SIZE, grid_size * self.SQUARE_SIZE
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Gobblet Game")
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

    def draw_board(self):
        self.screen.fill(self.WHITE)
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                pygame.draw.rect(self.screen, self.BLACK,
                                 (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE), 0)
                pygame.draw.rect(self.screen, self.WHITE,
                                 (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE), 1)

                if self.board[row][col] != ' ':
                    piece = self.board[row][col]
                    pygame.draw.circle(self.screen, (255, 0, 0) if piece == 'X' else (0, 0, 255),
                                       (col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2,
                                        row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2),
                                       self.SQUARE_SIZE // 3)

        pygame.display.flip()

    def check_win(self, player):
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

    def evaluate_board(self):
        if self.check_win('X'):
            return 1
        elif self.check_win('O'):
            return -1
        elif self.check_draw():
            return 0

        return None

    def check_draw(self):
        return all(self.board[row][col] != ' ' for row in range(self.GRID_SIZE) for col in range(self.GRID_SIZE))

# Example Usage:
# game_board = GameBoard(grid_size=4)
# game_board.draw_board()
# time.sleep(5)
# pygame.quit()
# sys.exit()
