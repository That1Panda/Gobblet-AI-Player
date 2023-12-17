import time
from gameBoard import GameBoard
import copy
    

class AIAlgorithms:
    def scoring(board: GameBoard):
        bounse = 0
        max_score = 0
        for row in range(board.GRID_SIZE):
            score = 0
            for col in range(board.GRID_SIZE):
                if board.board[row][col] == 'X':
                    score += 1
                else:
                    score = 0
                    break
            if score == 3: bounse += 1
            max_score =max(max_score,score)
            
        for col in range(board.GRID_SIZE):
            score = 0
            for row in range(board.GRID_SIZE):
                if board.board[row][col] == 'X':
                    score += 1
                elif board.board[row][col] != ' ':
                    score = 0
                    break
            if score == 3: bounse += 1
            max_score =max(max_score,score)
        
        score = 0
        for i in range(board.GRID_SIZE):
            if board.board[i][i] == 'X':
                score += 1
            elif board.board[i][i] != ' ':
                score = 0
                break
        if score == 3: bounse += 1
        max_score =max(max_score,score)
        
        score = 0
        for i in range(board.GRID_SIZE):
            if board.board[i][board.GRID_SIZE-1-i] == 'X':
                score += 1
            elif board.board[i][board.GRID_SIZE-1-i] != ' ':
                score = 0
                break
        if score == 3: bounse += 1
        max_score =max(max_score,score)
        
        Obounse = 0
        Omax_score = 0
        for row in range(board.GRID_SIZE):
            score = 0
            for col in range(board.GRID_SIZE):
                if board.board[row][col] == 'O':
                    score += 1
                else:
                    score = 0
                    break
            if score == 3: Obounse += 1
            Omax_score =max(Omax_score,score)
            
        for col in range(board.GRID_SIZE):
            score = 0
            for row in range(board.GRID_SIZE):
                if board.board[row][col] == 'O':
                    score += 1
                elif board.board[row][col] != ' ':
                    score = 0
                    break
            if score == 3: Obounse += 1
            Omax_score =max(Omax_score,score)
        
        score = 0
        for i in range(board.GRID_SIZE):
            if board.board[i][i] == 'O':
                score += 1
            elif board.board[i][i] != ' ':
                score = 0
                break
        if score == 3: Obounse += 1
        Omax_score =max(Omax_score,score)
        
        score = 0
        for i in range(board.GRID_SIZE):
            if board.board[i][board.GRID_SIZE-1-i] == 'O':
                score += 1
            elif board.board[i][board.GRID_SIZE-1-i] != ' ':
                score = 0
                break
        if score == 3: Obounse += 1
        Omax_score =max(Omax_score,score)
        
        if (max_score + bounse ) > (Omax_score + Obounse):
            return (max_score + bounse)
        else:
            return -(Omax_score + Obounse)

    @staticmethod
    def alpha_beta_pruning(self, board: GameBoard,depth, max_depth: int, is_maximizing: bool, current_player: str, alpha, beta, start_time:float, time_limit:float ) -> int:

    # def alpha_beta_pruning(self, board: GameBoard,depth, max_depth: int, is_maximizing: bool, current_player: str, alpha, beta) -> int:
        """
        Performs the alpha_beta_pruning algorithm and returns the score of the board.

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
            return self.scoring(board)/depth, board
            # return score, board
        # if depth == max_depth:
        #     return 0, board
        # score = self.scoring(board)
        # # if score is not None:
        # if score == 4 or score == -4:
        
        if depth == max_depth:
            return self.scoring(board)/depth, board
            return 0, board
            # return self.scoring(board)/ depth, board


        if is_maximizing:
            max_eval = float('-inf') #alpha
            best_board = GameBoard(grid_size=4) 
            best_board.board = copy.deepcopy(board.board)
            for row in range(board.GRID_SIZE):
                for col in range(board.GRID_SIZE):
                    if board.board[row][col] == ' ':
                        board.board[row][col] = current_player
                        eval_score, temp_board = AIAlgorithms.alpha_beta_pruning(self, board, depth + 1, max_depth, False,'X' if current_player == 'O' else 'O',alpha, beta, start_time, time_limit )
                        if(max_eval < eval_score):
                            max_eval = eval_score 
                            best_board.board = copy.deepcopy(board.board)
                        board.board[row][col] = ' '  # Undo the move

                        alpha = max(alpha, eval_score)
                        if beta <= alpha:
                            break  # Beta cutoff
                        
                        if time.time() - start_time > time_limit:
                            print(f"Time limit ({time_limit} seconds) exceeded. Terminating search.")
                            return max_eval, best_board 

            return max_eval, best_board
        
        else:
            min_eval = float('inf')
            best_board = GameBoard(grid_size=4) 
            best_board.board = board.board.copy()
            
            for row in range(board.GRID_SIZE):
                for col in range(board.GRID_SIZE):
                    if board.board[row][col] == ' ':
                        board.board[row][col] = current_player
                        eval_score, temp_board = AIAlgorithms.alpha_beta_pruning(self, board, depth + 1, max_depth, True, 'X' if current_player == 'O' else 'O', alpha, beta, start_time, time_limit)
                        
                        if(min_eval > eval_score):
                            min_eval = eval_score 
                            best_board.board = copy.deepcopy(board.board)
                        board.board[row][col] = ' '  # Undo the move
                        
                        beta = min(beta, eval_score)
                        if beta <= alpha:
                            break  # Alpha cutoff
                        
                        if time.time() - start_time > time_limit:
                            print(f"Time limit ({time_limit} seconds) exceeded. Terminating search.")
                            return min_eval, best_board
                        
                        
                        # min_eval = min(min_eval, eval_score)
                    if beta <= alpha:
                            break  # Alpha cutoff
            return min_eval, best_board
        
    @staticmethod
    def get_best_move(self, board, is_max, player, time_limit=5):
        start_time = time.time()
        depth = 1
        best_move = None
        t = time.time()
        if player == 'X':
            best_val = float('-inf')
        else:
            best_val = float('inf')
        
        while time.time() - start_time < time_limit:

            if best_move:
                print(f"Depth {depth - 1} completed in {time.time() - start_time:.2f} seconds")

            val, move = self.alpha_beta_pruning(self, board, 0, depth, is_max, player, float('-inf'),float('inf'), t, time_limit)
            
            print("val: " + str(val) + ", best: " + str(best_val))
            print(move.board)
            if time.time() - start_time <= time_limit:
                print(f"Time inside decision: {time.time() - start_time:.2f} seconds")
                best_move = move
                best_val = val 
            depth += 1
        print(f"Interrupted Depth {depth - 1} completed in {time.time() - start_time:.2f} seconds")
        print("best: " + str(best_move.board))
        return best_val, best_move

                
AI = AIAlgorithms

board = GameBoard(grid_size=4) 
bb = GameBoard(grid_size=4)
bb.board = copy.deepcopy(board.board)
board.board[0][0] = 'X'
board.board[1][0] = 'X'

board.board[0][1] = 'O'
board.board[1][1] = 'O'

board.board = [[' ', ' ', ' ', ' '], 
               [' ', 'O', 'O', 'X'], 
               [' ', 'O', ' ', 'X'],
               [' ', 'X', ' ', ' ']]

# board.board = [[' ', ' ', ' ', 'O'], 
#                [' ', 'O', 'O', 'X'], 
#                [' ', 'O', ' ', 'X'],
#                ['X', 'X', 'O', 'X']]
# board.board = [['O', ' ', ' ', 'X'], 
#                ['O', ' ', 'X', 'X'], 
#                ['X', ' ', 'X', 'X'],
#                ['O', ' ', 'X', 'O']]

# board.board = [[' ', ' ', ' ', 'X'], 
#                [' ', ' ', ' ', 'X'], 
#                [' ', ' ', ' ', 'X'],
#                [' ', 'X', 'X', ' ']]



print(AI.scoring(board))
# mmx,board= AI.alpha_beta_pruning(board, 4, True, 'X')

mmx,board= AI.get_best_move(AI,board,True, 'X', 15)
mmx,board= AI.get_best_move(AI,board,False, 'O', 15)
mmx,board= AI.get_best_move(AI,board,True, 'X', 15)
mmx,board= AI.get_best_move(AI,board,False, 'O', 15)
mmx,board= AI.get_best_move(AI,board,True, 'X', 15)
mmx,board= AI.get_best_move(AI,board,False, 'O', 15)
mmx,board= AI.get_best_move(AI,board,True, 'X', 15)
mmx,board= AI.get_best_move(AI,board,False, 'O', 15)
mmx,board= AI.get_best_move(AI,board,True, 'X', 15)
mmx,board= AI.get_best_move(AI,board,False, 'O', 5)
mmx,board= AI.get_best_move(AI,board,True, 'X', 5)
mmx,board= AI.get_best_move(AI,board,False, 'O', 5)

# # print(board.board)
mmo, board = AI.alpha_beta_pruning(AI, board,0,  4, True, 'X',float('-inf'),float('inf'))
# # print(board.board)
# mmx,board= AI.alpha_beta_pruning(board, 0, True, 'X')
# # print(board.board)
# mmo, board = AI.alpha_beta_pruning(board, 0, False, 'O')
# # print(board.board)
# mmx,board= AI.alpha_beta_pruning(board, 0, True, 'X')
# # print(board.board)
# mmo, board = AI.alpha_beta_pruning(board, 0, False, 'O')
# # print(board.board)
# mmx,board= AI.alpha_beta_pruning(board, 0, True, 'X')
# # print(board.board)
# mmo, board = AI.alpha_beta_pruning(board, 0, False, 'O')
# # print(board.board)
# mmx,board= AI.alpha_beta_pruning(board, 0, True, 'X')
# mmo, board = AI.alpha_beta_pruning(board, 0, False, 'O')
# mmx,board= AI.alpha_beta_pruning(board, 0, True, 'X')
# mmo, board = AI.alpha_beta_pruning(board, 0, False, 'O')
# print(mmx)