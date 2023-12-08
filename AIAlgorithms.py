class AIAlgorithms:
    @staticmethod
    def minimax(board, depth, is_maximizing, current_player):
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
    def alpha_beta_pruning(board, depth, alpha, beta, is_maximizing, current_player):
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
    def alpha_beta_pruning_iterative_deepening(board, max_depth, current_player):
        best_move = None
        alpha = float('-inf')
        beta = float('inf')

        for depth in range(1, max_depth + 1):
            move, _ = AIAlgorithms.alpha_beta_pruning_helper(board, depth, alpha, beta, True, current_player)
            best_move = move

        return best_move

    @staticmethod
    def alpha_beta_pruning_helper(board, depth, alpha, beta, is_maximizing, current_player):
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
