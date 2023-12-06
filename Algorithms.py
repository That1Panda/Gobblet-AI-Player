import random 

# Class containing all the algorithms
class Algorithms:
    """
    A class containing all the algorithms.

    Attributes:
        board (list[list[str]]): a list of lists representing the game board
        GRID_SIZE (int): the size of the board
    """
    def __init__(self,board,GRID_SIZE):
        self.board = board
        self.GRID_SIZE = GRID_SIZE

    def random_move(self):
        """
        Performs a random move.

        Returns:
            tuple: a tuple representing the row and column of the move
        """

        empty_cells = [(row, col) for row in range(self.GRID_SIZE) for col in range(self.GRID_SIZE) if self.board[row][col] == ' ']
        return random.choice(empty_cells)
    
    def check_win(self,current_player):
        """
        Checks if the player has won the game.

        Args:
            player (str): a string representing the player which is either 'X' or 'O'

        Returns:
            bool: True if the player has won the game, False otherwise
        """
        for row in range(self.GRID_SIZE):
            if all(self.board[row][col] == current_player for col in range(self.GRID_SIZE)):
                return True

        for col in range(self.GRID_SIZE):
            if all(self.board[row][col] == current_player for row in range(self.GRID_SIZE)):
                return True

        if all(self.board[i][i] == current_player for i in range(self.GRID_SIZE)) or all(self.board[i][self.GRID_SIZE - i - 1] == player for i in range(self.GRID_SIZE)):
            return True

        return False
    
    def check_draw(self):
        """
        Checks if the game is a draw.

        Returns:
            bool: True if the game is a draw, False otherwise
        """
        return all(self.board[row][col] != ' ' for row in range(self.GRID_SIZE) for col in range(self.GRID_SIZE))

    def evaluate_board(self):
        """
        Evaluates the score of the board.

        Returns:
            bool: +1 if 'X' wins, -1 if 'O' wins, 0 if draw or ongoing game
        """
        if self.check_win('X'):
            return 1
        elif self.check_win('O'):
            return -1
        elif self.check_draw():
            return 0

        return None
    
    

    def minimax(self,depth, is_maximizing, current_player):
        """
        Performs the Minimax algorithm and returns the score of the board.

        Args:
            depth (int): the depth of the current node in the game tree
            is_maximizing (bool): True if the current node is a maximizing node, False otherwise
            current_player (str): a string representing the current player which is either 'X' or 'O'

        Returns:
            min_eval (int): the score of the board
        """
        score = self.evaluate_board()

        if score is not None:
            return score

        if is_maximizing:
            max_eval = float('-inf')
            for row in range(self.GRID_SIZE):
                for col in range(self.GRID_SIZE):
                    if self.board[row][col] == ' ':
                        self.board[row][col] = current_player
                        eval_score = self.minimax(depth + 1, False, 'X' if current_player == 'O' else 'O')
                        self.board[row][col] = ' '
    
                        max_eval = max(max_eval, eval_score)
            return max_eval 
        else:
            min_eval = float('inf')
            for row in range(self.GRID_SIZE):
                for col in range(self.GRID_SIZE):
                    if self.board[row][col] == ' ':
                        self.board[row][col] = current_player
                        eval_score = self.minimax(depth + 1, True, 'X' if current_player == 'O' else 'O')
                        self.board[row][col] = ' '
    
                        min_eval = min(min_eval, eval_score)
            return min_eval
        
    def alpha_beta_pruning(self,depth, alpha, beta, is_maximizing):
        """
        Performs the Alpha-Beta Pruning algorithm and returns the score of the board.

        Args:
            depth (int): the depth of the current node in the game tree
            alpha (float): the best value that the maximizing player can guarantee at the current level or above
            beta (float): the best value that the minimizing player can guarantee at the current level or above
            is_maximizing (bool): True if the current node is a maximizing node, False otherwise

        Returns:
            int: the score of the board
        """
        score = self.evaluate_board()

        if score is not None:
            return score

        if is_maximizing:
            max_eval = float('-inf')
            for row in range(self.GRID_SIZE):
                for col in range(self.GRID_SIZE):
                    if self.board[row][col] == ' ':
                        self.board[row][col] = 'X'
                        eval_score = self.alpha_beta_pruning(depth + 1, alpha, beta, False)
                        self.board[row][col] = ' '

                        max_eval = max(max_eval, eval_score)
                        alpha = max(alpha, eval_score)
                        if beta <= alpha:
                            break
            return max_eval
        else:
            min_eval = float('inf')
            for row in range(self.GRID_SIZE):
                for col in range(self.GRID_SIZE):
                    if self.board[row][col] == ' ':
                        self.board[row][col] = 'O'
                        eval_score = self.alpha_beta_pruning(depth + 1, alpha, beta, True)
                        self.board[row][col] = ' '

                        min_eval = min(min_eval, eval_score)
                        beta = min(beta, eval_score)
                        if beta <= alpha:
                            break
            return min_eval
        
    def alpha_beta_pruning_iterative_deepening(self,max_depth):
        """
        Performs Alpha-Beta Pruning with Iterative Deepening.

        Args:
            max_depth (int): the maximum depth to explore

        Returns:
            best_move (tuple): a tuple representing the row and column of the best move
        """
        best_move = None
        alpha = float('-inf')
        beta = float('inf')

        for depth in range(1, max_depth + 1):
            move, _ = self.alpha_beta_pruning_helper(depth, alpha, beta, True)
            best_move = move

        return best_move
    
    def alpha_beta_pruning_helper(self,depth, alpha, beta, is_maximizing):
        """
        Helper function for Alpha-Beta Pruning with Iterative Deepening.

        Args:
            depth int: the depth of the current node in the game tree
            alpha float: the best value that the maximizing player can guarantee at the current level or above
            beta float: the best value that the minimizing player can guarantee at the current level or above
            is_maximizing bool: True if the current node is a maximizing node, False otherwise

        Returns:
            best_move (tuple): a tuple representing the row and column of the best move, and the score
            max_eval/min_eval (int): the score of the board
        """
        score = self.evaluate_board()

        if score is not None or depth == 0:
            return None, score

        best_move = None

        if is_maximizing:
            max_eval = float('-inf')
            for row in range(self.GRID_SIZE):
                for col in range(self.GRID_SIZE):
                    if self.board[row][col] == ' ':
                        self.board[row][col] = 'X'
                        _, eval_score = self.alpha_beta_pruning_helper(depth - 1, alpha, beta, False)
                        self.board[row][col] = ' '

                        if eval_score > max_eval:
                            max_eval = eval_score
                            best_move = (row, col)

                        alpha = max(alpha, eval_score)
                        if beta <= alpha:
                            break

            return best_move, max_eval
        else:
            min_eval = float('inf')
            for row in range(self.GRID_SIZE):
                for col in range(self.GRID_SIZE):
                    if self.board[row][col] == ' ':
                        self.board[row][col] = 'O'
                        _, eval_score = self.alpha_beta_pruning_helper(depth - 1, alpha, beta, True)
                        self.board[row][col] = ' '

                        if eval_score < min_eval:
                            min_eval = eval_score
                            best_move = (row, col)

                        beta = min(beta, eval_score)
                        if beta <= alpha:
                            break

            return best_move, min_eval

    # make alpha beta pruning with iterative deepening depending on current player
    