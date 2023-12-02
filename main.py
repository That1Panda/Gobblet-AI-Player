import pygame
import sys
import random

# Constants
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 4
SQUARE_SIZE = WIDTH // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Function to draw the board
def draw_board():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            pygame.draw.rect(screen, WHITE, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 0)
            pygame.draw.rect(screen, BLACK, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)

            if board[row][col] != ' ':
                piece = board[row][col]
                pygame.draw.circle(screen, (255, 0, 0) if piece == 'X' else (0, 0, 255),
                                   (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   SQUARE_SIZE // 3)

# Function to check for a win
def check_win(player):
    for row in range(GRID_SIZE):
        if all(board[row][col] == player for col in range(GRID_SIZE)):
            return True

    for col in range(GRID_SIZE):
        if all(board[row][col] == player for row in range(GRID_SIZE)):
            return True

    if all(board[i][i] == player for i in range(GRID_SIZE)) or all(board[i][GRID_SIZE - i - 1] == player for i in range(GRID_SIZE)):
        return True

    return False

# Function to make a move for the computer player
def computer_move():
    empty_cells = [(row, col) for row in range(GRID_SIZE) for col in range(GRID_SIZE) if board[row][col] == ' ']
    if empty_cells:
        return random.choice(empty_cells)
    return None

# Function to handle the main game loop
def play_game(player1_type, player2_type):
    current_player = 'X'
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and current_player == 'X' and player1_type == 'human':
                mouseX, mouseY = pygame.mouse.get_pos()
                clicked_row, clicked_col = mouseY // SQUARE_SIZE, mouseX // SQUARE_SIZE

                if board[clicked_row][clicked_col] == ' ':
                    board[clicked_row][clicked_col] = current_player

                    if check_win(current_player):
                        print(f"Player {current_player} wins!")
                        running = False

                    current_player = 'O'

            if event.type == pygame.MOUSEBUTTONDOWN and current_player == 'O' and player2_type == 'human':
                mouseX, mouseY = pygame.mouse.get_pos()
                clicked_row, clicked_col = mouseY // SQUARE_SIZE, mouseX // SQUARE_SIZE

                if board[clicked_row][clicked_col] == ' ':
                    board[clicked_row][clicked_col] = current_player

                    if check_win(current_player):
                        print(f"Player {current_player} wins!")
                        running = False

                    current_player = 'X'

        if current_player == 'X' and player1_type == 'computer':
            computer_move_result = computer_move()
            if computer_move_result:
                row, col = computer_move_result
                board[row][col] = current_player

                if check_win(current_player):
                    print(f"Player {current_player} wins!")
                    running = False

                current_player = 'O'

        elif current_player == 'O' and player2_type == 'computer':
            computer_move_result = computer_move()
            if computer_move_result:
                row, col = computer_move_result
                board[row][col] = current_player

                if check_win(current_player):
                    print(f"Player {current_player} wins!")
                    running = False

                current_player = 'X'

        # Draw the board
        screen.fill(WHITE)
        draw_board()

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()
    sys.exit()

# Function to ask for the game mode
def choose_game_mode():
    print("Choose game mode:")
    print("1. Human vs. Human")
    print("2. Human vs. Computer")
    print("3. Computer vs. Human")
    print("4. Computer vs. Computer")

    choice = input("Enter the number of your choice: ")
    return choice

# Main code
game_mode = choose_game_mode()

# Set player types based on the chosen game mode
if game_mode == '1':
    player1_type, player2_type = 'human', 'human'
elif game_mode == '2':
    player1_type, player2_type = 'human', 'computer'
elif game_mode == '3':
    player1_type, player2_type = 'computer', 'human'
else:
    player1_type, player2_type = 'computer', 'computer'

# Initialize Pygame window
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gobblet Game")

# Initialize the game board
board = [[' ' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Start the game
play_game(player1_type, player2_type)
