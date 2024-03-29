import sys
import random
import time
import pygame

# Constants
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 4
SQUARE_SIZE = WIDTH // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Function to draw the board
def draw_board():
    """
    Draws the board on the screen.
    """
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            pygame.draw.rect(screen, BLACK, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 0)
            pygame.draw.rect(screen, WHITE, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)

            if board[row][col] != ' ':
                piece = board[row][col]
                pygame.draw.circle(screen, (255, 0, 0) if piece == 'X' else (0, 0, 255),
                                   (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   SQUARE_SIZE // 3)

# Function to check for a win
def check_win(player):
    """
    Checks if the player has won the game.

    Args:
        player (str): a string representing the player which is either 'X' or 'O'

    Returns:
        bool: True if the player has won the game, False otherwise
    """
    for row in range(GRID_SIZE):
        if all(board[row][col] == player for col in range(GRID_SIZE)):
            return True

    for col in range(GRID_SIZE):
        if all(board[row][col] == player for row in range(GRID_SIZE)):
            return True

    if all(board[i][i] == player for i in range(GRID_SIZE)) or all(board[i][GRID_SIZE - i - 1] == player for i in range(GRID_SIZE)):
        return True

    return False

# Function to evaluate the score of the board
def evaluate_board():
    """
    Evaluates the score of the board.

    Returns:
        bool: +1 if 'X' wins, -1 if 'O' wins, 0 if draw or ongoing game
    """
    if check_win('X'):
        return 1
    elif check_win('O'):
        return -1
    elif check_draw():
        return 0

    return None


# Function to perform the Minimax algorithm
def minimax(board, depth, is_maximizing, current_player):
    """
    Performs the Minimax algorithm and returns the score of the board.

    Args:
        board (GameBoard): a list of lists representing the game board
        depth (int): the depth of the current node in the game tree
        is_maximizing (bool): True if the current node is a maximizing node, False otherwise
        current_player (str): a string representing the current player which is either 'X' or 'O'

    Returns:
        min_eval (int): the score of the board
    """
    score = evaluate_board()

    if score is not None:
        return score

    if is_maximizing:
        max_eval = float('-inf')
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if board[row][col] == ' ':
                    board[row][col] = current_player
                    eval_score = minimax(board, depth + 1, False, 'X' if current_player == 'O' else 'O')
                    board[row][col] = ' '  # Undo the move

                    max_eval = max(max_eval, eval_score)
        return max_eval
    else:
        min_eval = float('inf')
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if board[row][col] == ' ':
                    board[row][col] = current_player
                    eval_score = minimax(board, depth + 1, True, 'X' if current_player == 'O' else 'O')
                    board[row][col] = ' '  # Undo the move

                    min_eval = min(min_eval, eval_score)
        return min_eval
    
def alpha_beta_pruning(board, depth, alpha, beta, is_maximizing, current_player):
    """
    Performs the Alpha-Beta Pruning algorithm and returns the score of the board.

    Args:
        board (GameBoard): a list of lists representing the game board
        depth (int): the depth of the current node in the game tree
        alpha (float): the best value that the maximizing player can guarantee at the current level or above
        beta (float): the best value that the minimizing player can guarantee at the current level or above
        is_maximizing (bool): True if the current node is a maximizing node, False otherwise
        current_player (str): a string representing the current player which is either 'X' or 'O'

    Returns:
        int: the score of the board
    """
    score = evaluate_board()

    if score is not None:
        return score

    if is_maximizing:
        max_eval = float('-inf')
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if board[row][col] == ' ':
                    board[row][col] = current_player
                    eval_score = alpha_beta_pruning(board, depth + 1, alpha, beta, False, 'X' if current_player == 'O' else 'O')
                    board[row][col] = ' '  # Undo the move

                    max_eval = max(max_eval, eval_score)
                    alpha = max(alpha, eval_score)
                    if beta <= alpha:
                        break  # Beta cutoff
        return max_eval
    else:
        min_eval = float('inf')
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if board[row][col] == ' ':
                    board[row][col] = current_player
                    eval_score = alpha_beta_pruning(board, depth + 1, alpha, beta, True, 'X' if current_player == 'O' else 'O')
                    board[row][col] = ' '  # Undo the move

                    min_eval = min(min_eval, eval_score)
                    beta = min(beta, eval_score)
                    if beta <= alpha:
                        break  # Alpha cutoff
        return min_eval

def alpha_beta_pruning_iterative_deepening(board, max_depth, current_player):
    """
    Performs Alpha-Beta Pruning with Iterative Deepening.

    Args:
        board (GameBoard): a list of lists representing the game board
        max_depth (int): the maximum depth to explore
        current_player (str): a string representing the current player which is either 'X' or 'O'

    Returns:
        best_move (tuple): a tuple representing the row and column of the best move
    """
    best_move = None
    alpha = float('-inf')
    beta = float('inf')

    for depth in range(1, max_depth + 1):
        move, _ = alpha_beta_pruning_helper(board, depth, alpha, beta, True, current_player)
        best_move = move

    return best_move

def alpha_beta_pruning_helper(board, depth, alpha, beta, is_maximizing, current_player):
    """
    Helper function for Alpha-Beta Pruning with Iterative Deepening.

    Args:
        board GameBoard: a list of lists representing the game board
        depth int: the depth of the current node in the game tree
        alpha float: the best value that the maximizing player can guarantee at the current level or above
        beta float: the best value that the minimizing player can guarantee at the current level or above
        is_maximizing bool: True if the current node is a maximizing node, False otherwise
        current_player (str): a string representing the current player which is either 'X' or 'O'

    Returns:
        best_move (tuple): a tuple representing the row and column of the best move, and the score
        max_eval/min_eval (int): the score of the board
    """
    score = evaluate_board()

    if score is not None or depth == 0:
        return None, score

    best_move = None

    if is_maximizing:
        max_eval = float('-inf')
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if board[row][col] == ' ':
                    board[row][col] = current_player
                    _, eval_score = alpha_beta_pruning_helper(board, depth - 1, alpha, beta, False, 'X' if current_player == 'O' else 'O')
                    board[row][col] = ' '  # Undo the move

                    if eval_score > max_eval:
                        max_eval = eval_score
                        best_move = (row, col)

                    alpha = max(alpha, eval_score)
                    if beta <= alpha:
                        break  # Beta cutoff

        return best_move, max_eval
    else:
        min_eval = float('inf')
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if board[row][col] == ' ':
                    board[row][col] = current_player
                    _, eval_score = alpha_beta_pruning_helper(board, depth - 1, alpha, beta, True, 'X' if current_player == 'O' else 'O')
                    board[row][col] = ' '  # Undo the move

                    if eval_score < min_eval:
                        min_eval = eval_score
                        best_move = (row, col)

                    beta = min(beta, eval_score)
                    if beta <= alpha:
                        break  # Alpha cutoff

        return best_move, min_eval


# Function to make a move for the computer player
def computer_move(current_player='X',algo='random'):
    """
    Chooses the next a move for the computer player.
    
    Args:
        algo (str): a string representing the algorithm to be used which is either 'random' or 'minimax'
        current_player (str): a string representing the current player which is either 'X' or 'O'
        
    Returns:
        best_move (tuple): a tuple representing the row and column of the chosen cell else None if the board is full
    """
    empty_cells = [(row, col) for row in range(GRID_SIZE) for col in range(GRID_SIZE) if board[row][col] == ' ']

    if empty_cells and algo == 'random':
        return random.choice(empty_cells)
    
    elif empty_cells and algo == 'minimax':
        best_score = float('-inf')
        best_move = None

        for move in empty_cells:
            row, col = move
            board[row][col] = 'X'
            score = minimax(board, 0, False, 'X' if current_player == 'O' else 'O')
            board[row][col] = ' '  # Undo the move

            if score > best_score:
                best_score = score
                best_move = move

        return best_move
    return None

def check_draw():
    """
    Checks if the game is a draw.

    Returns:
        bool: True if the game is a draw, False otherwise
    """
    return all(board[row][col] != ' ' for row in range(GRID_SIZE) for col in range(GRID_SIZE))

def game_status(current_player):
    """
    Checks if the current player has won the game or the game is a draw.

    Args:
        current_player (str): a string representing the current player which is either 'X' or 'O'

    Returns:
        bool: False if the current player has won the game or the game is a draw, True otherwise
    """
    if check_win(current_player):
        print(f"Player {current_player} wins!")
        return False
    elif check_draw():
        print("It's a draw!")
        return False
    return True


def human_move(current_player):
    """
    Handles the human move. (NOT USED BECAUSE NOT WORKING)

    Args:
        current_player (str): a string representing the current player which is either 'X' or 'O'

    Returns:
        bool: False if the current player has won the game or the game is a draw, True otherwise
    """
    mouseX, mouseY = pygame.mouse.get_pos()
    clicked_row, clicked_col = mouseY // SQUARE_SIZE, mouseX // SQUARE_SIZE

    if board[clicked_row][clicked_col] == ' ':
        board[clicked_row][clicked_col] = current_player

        running = game_status(current_player)
        if current_player == 'X':
            return ('O', running)
        
        return  ('X', running)

# Function to handle the main game loop
def play_game(player1_type, player2_type, computer_delay=0):
    """
    Handles the main game loop.

    Args:
        player1_type (str): A string representing the type of player 1 which is either 'human' or 'computer'
        player2_type (str): A string representing the type of player 2 which is either 'human' or 'computer'
        computer_delay (int): The delay in seconds for the computer to make a move
    """
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

                    running = game_status(current_player)
                    current_player = 'O'

            if event.type == pygame.MOUSEBUTTONDOWN and current_player == 'O' and player2_type == 'human':
                mouseX, mouseY = pygame.mouse.get_pos()
                clicked_row, clicked_col = mouseY // SQUARE_SIZE, mouseX // SQUARE_SIZE

                if board[clicked_row][clicked_col] == ' ':
                    board[clicked_row][clicked_col] = current_player

                    running = game_status(current_player)
                    current_player = 'X'

        if current_player == 'X' and player1_type == 'computer':
            computer_move_result = computer_move(current_player=current_player)
            if computer_move_result:
                time.sleep(computer_delay)
                row, col = computer_move_result
                board[row][col] = current_player

                running = game_status(current_player)
                current_player = 'O'

        elif current_player == 'O' and player2_type == 'computer':
            computer_move_result = computer_move(current_player=current_player)
            if computer_move_result:
                time.sleep(computer_delay)
                row, col = computer_move_result
                board[row][col] = current_player

                running = game_status(current_player)
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
    """
    Asks the user to choose the game mode out of the four available modes.

    Returns:
        str: number representing the chosen game mode
    """
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
