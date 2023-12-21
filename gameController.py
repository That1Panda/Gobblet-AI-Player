from typing import Tuple
import pygame
import sys
import random
import time
import argparse
from player import Player
from gameBoard import GameBoard

class GameController:
    """
    A class representing the game controller.

    Attributes:
        player1 (Player): the first player
        player2 (Player): the second player
        current_player (Player): the current player
        board (GameBoard): the game board

    Methods:
        __init__(self, player1: Player, player2: Player):
            Initializes the game controller with the two players and the game board.

        switch_player(self):
            Switches the current player.

        play_game(self):
            Loops through the game until a player wins or it's a draw.

        game_status(self) -> bool:
            Checks the game status and returns True if the game is still running, False otherwise.
    """ 
    def __init__(self, player1: Player, player2: Player):
        """
        Initializes the game controller with the two players and the game board.

        Args:
            player1 (Player): the first player
            player2 (Player): the second player
        """
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.board = GameBoard(grid_size=6)
        self.board.draw_board(player1,player2)
        self.board.assign_initial_values(player1,player2)

    def switch_player(self):
        """
        Switches the current player.
        """
        self.current_player = self.player2 if self.current_player == self.player1 else self.player1

    def play_game(self):
        """
        Loops through the game until a player wins or it's a draw.
        """
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

            # Pass the player states to draw_board
            self.board.draw_board(self.player1, self.player2)
            move = False
            while move == False : 
                move = self.current_player.make_move(self.board)
                
            running, game_message = self.game_status()
            self.switch_player()
            pygame.display.flip()
        
        return game_message

    def game_status(self) -> Tuple[bool, str]:
        """
        Checks the game status and returns True if the game is still running, False otherwise.

        Returns:
            running (bool): True if the game is still running, False otherwise.
        """
        if self.board.check_win(self.current_player.symbol):
            print(f"Player {self.current_player.symbol} wins!")
            return False, f"{self.current_player.player_name} Player wins!"
        elif self.board.check_draw():
            print("It's a draw!")
            return False, "It's a draw!"
        return True, None

