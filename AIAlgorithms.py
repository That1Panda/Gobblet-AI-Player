from gameBoard import GameBoard
class AIAlgorithms:
    """
    A class containing static methods for AI algorithms in the game.

    Methods:
        minimax(board: GameBoard, depth: int, is_maximizing: bool, current_player: str) -> int:
            Performs the Minimax algorithm and returns the score of the board.

        alpha_beta_pruning(board: GameBoard, depth: int, alpha: float, beta: float,
                           is_maximizing: bool, current_player: str) -> int:
            Performs the Alpha-Beta Pruning algorithm and returns the score of the board.

        alpha_beta_pruning_iterative_deepening(board: GameBoard, max_depth: int,
                                               current_player: str) -> tuple(int, int):
            Performs the Alpha-Beta Pruning algorithm with iterative deepening and returns the best move.

        alpha_beta_pruning_helper(board: GameBoard, depth: int, alpha: float, beta: float,
                                  is_maximizing: bool, current_player: str) -> tuple(tuple(int, int), int):
            Helper function for Alpha-Beta Pruning with Iterative Deepening.
    """

    @staticmethod
    def minimax(board: GameBoard, depth: int, is_maximizing: bool, current_player: str) -> int:
        """
        Performs the Minimax algorithm and returns the score of the board.

        Args:
            board (GameBoard): a list of lists representing the game board
            depth (int): the depth of the current node in the game tree
            is_maximizing (bool): True if the current node is a maximizing node, False otherwise
            current_player (str): a string representing the current player which is either 'X' or 'O'

        Returns:
            min_eval/max_val (int): the score of the board
        """
        score = board.evaluate_board()

        if score is not None:
            return score

        if is_maximizing:
            max_eval = float('-inf')
            for row in range(board.GRID_SIZE):
                for col in range(board.GRID_SIZE):
                    if board.board[row][col] == ' ':
                        board.board[row][col] = current_player
                        eval_score = AIAlgorithms.minimax(board, depth + 1, False, 'X' if current_player == 'O' else 'O')
                        board.board[row][col] = ' '  # Undo the move

                        max_eval = max(max_eval, eval_score)
            return max_eval
        else:
            min_eval = float('inf')
            for row in range(board.GRID_SIZE):
                for col in range(board.GRID_SIZE):
                    if board.board[row][col] == ' ':
                        board.board[row][col] = current_player
                        eval_score = AIAlgorithms.minimax(board, depth + 1, True, 'X' if current_player == 'O' else 'O')
                        board.board[row][col] = ' '  # Undo the move

                        min_eval = min(min_eval, eval_score)
            return min_eval

    @staticmethod
    def alpha_beta_pruning(board: GameBoard, depth: int, alpha: float, beta: float,
                           is_maximizing: bool, current_player: str) -> int:
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
            min_eval/max_val (int): the score of the board
        """
        score = board.evaluate_board()

        if score is not None:
            return score

        if is_maximizing:
            max_eval = float('-inf')
            for row in range(board.GRID_SIZE):
                for col in range(board.GRID_SIZE):
                    if board.board[row][col] == ' ':
                        board.board[row][col] = current_player
                        eval_score = AIAlgorithms.alpha_beta_pruning(board, depth + 1, alpha, beta, False,
                                                                     'X' if current_player == 'O' else 'O')
                        board.board[row][col] = ' '  # Undo the move

                        max_eval = max(max_eval, eval_score)
                        alpha = max(alpha, eval_score)
                        if beta <= alpha:
                            break  # Beta cutoff
            return max_eval
        else:
            min_eval = float('inf')
            for row in range(board.GRID_SIZE):
                for col in range(board.GRID_SIZE):
                    if board.board[row][col] == ' ':
                        board.board[row][col] = current_player
                        eval_score = AIAlgorithms.alpha_beta_pruning(board, depth + 1, alpha, beta, True,
                                                                     'X' if current_player == 'O' else 'O')
                        board.board[row][col] = ' '  # Undo the move

                        min_eval = min(min_eval, eval_score)
                        beta = min(beta, eval_score)
                        if beta <= alpha:
                            break  # Alpha cutoff
            return min_eval

    @staticmethod
    def alpha_beta_pruning_iterative_deepening(board: GameBoard, max_depth: int,
                                               current_player: str) -> tuple:
        """
        Performs the Alpha-Beta Pruning algorithm with iterative deepening and returns the best move.

        Args:
            board (GameBoard): a list of lists representing the game board
            max_depth (int): the maximum depth to explore
            current_player (str): a string representing the current player which is either 'X' or 'O'

        Returns:
            best_move (tuple(int, int)): the best move to make
        """
        best_move = None
        alpha = float('-inf')
        beta = float('inf')

        for depth in range(1, max_depth + 1):
            move, _ = AIAlgorithms.alpha_beta_pruning_helper(board, depth, alpha, beta, True, current_player)
            best_move = move

        return best_move

    @staticmethod
    def alpha_beta_pruning_helper(board: GameBoard, depth: int, alpha: float, beta: float,
                                  is_maximizing: bool, current_player: str) -> tuple:
        """
        Helper function for Alpha-Beta Pruning with Iterative Deepening.

        Args:
            board (GameBoard): a list of lists representing the game board
            depth (int): the depth of the current node in the game tree
            alpha (float): the best value that the maximizing player can guarantee at the current level or above
            beta (float): the best value that the minimizing player can guarantee at the current level or above
            is_maximizing (bool): True if the current node is a maximizing node, False otherwise
            current_player (str): a string representing the current player which is either 'X' or 'O'

        Returns:
            best_move (tuple(int, int)): the best move to make
            min_eval/max_val (int): the score of the board
        """
        score = board.evaluate_board()

        if score is not None or depth == 0:
            return None, score

        best_move = None

        if is_maximizing:
            max_eval = float('-inf')
            for row in range(board.GRID_SIZE):
                for col in range(board.GRID_SIZE):
                    if board.board[row][col] == ' ':
                        board.board[row][col] = current_player
                        _, eval_score = AIAlgorithms.alpha_beta_pruning_helper(board, depth - 1, alpha, beta, False,
                                                                               'X' if current_player == 'O' else 'O')
                        board.board[row][col] = ' '  # Undo the move

                        if eval_score > max_eval:
                            max_eval = eval_score
                            best_move = (row, col)

                        alpha = max(alpha, eval_score)
                        if beta <= alpha:
                            break  # Beta cutoff

            return best_move, max_eval
        else:
            min_eval = float('inf')
            for row in range(board.GRID_SIZE):
                for col in range(board.GRID_SIZE):
                    if board.board[row][col] == ' ':
                        board.board[row][col] = current_player
                        _, eval_score = AIAlgorithms.alpha_beta_pruning_helper(board, depth - 1, alpha, beta, True,
                                                                               'X' if current_player == 'O' else 'O')
                        board.board[row][col] = ' '  # Undo the move

                        if eval_score < min_eval:
                            min_eval = eval_score
                            best_move = (row, col)

                        beta = min(beta, eval_score)
                        if beta <= alpha:
                            break  # Alpha cutoff

            return best_move, min_eval
