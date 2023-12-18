import time
from gameBoard import GameBoard
import copy

class move:
    """class of objects that contain the information about move to be done
    """
    def __init__(self, crow, ccol, node, nrow, ncol) -> None:
        self.curRow = crow
        self.curCol = ccol
        self.node = node
        self.newRow = nrow
        self.newCol = ncol
        pass

class AIAlgorithms:
    """
    A class containing static methods for AI algorithm in the game.

    Methods:

        get_best_move(self, board: GameBoard, is_max: bool, player: str, diffcult: int, time_limit:int=5):
            get best moves in certain time and diffcult

        alpha_beta_pruning(self, board: GameBoard,depth, max_depth: int, is_maximizing: bool, 
                            current_player: str, alpha, beta, start_time:float, time_limit:float ) -> int:      
            Performs the Alpha-Beta Pruning algorithm and returns the score of the board.

        def scoring(board: GameBoard):
            get the score if the search get to final level without any winning or loss

       Undo(currentBoatd : GameBoard, move: move):
            Undo this move from the board
            
        Generate_nextBoard(currentBoatd : GameBoard, move: move):
            generate the board after a move
            
        possiblePosition(board: GameBoard, curmove: move):
            is this position is able to apply this move

        gobblet_exist(board: GameBoard, crow: int,ccol: int, palyer_type: str):
            check if the gobblet at this position is able to move by player
      
        get_nextMoves(self, board: GameBoard , palyer_type : str):
            get all possible moves for player_type from this current voard

    """
    def __init__(self) -> None:
        pass

    
    @staticmethod
    def get_nextMoves(self, board: GameBoard , palyer_type : str):
        """get all possible moves for player_type from this current voard

        Args:
            board (GameBoard): current board before move
            palyer_type (str): the player which is 'X' or 'O'

        Returns:
            moves: return list of possible moves from this current board
        """
        moves = []
        #get current gobblet
        for crow in range(board.GRID_SIZE):
            for ccol in range(board.GRID_SIZE):
                #check if this position contain a free globblet of my own to be move
                if self.gobblet_exist(board, crow,ccol, palyer_type):
                    #get next position
                    for nrow in range(board.GRID_SIZE):
                        for ncol in range(board.GRID_SIZE):
                            curmove = move(crow,ccol,palyer_type,nrow,ncol)
                            # if this position can be occupt by the current gobblet
                            if self.possiblePosition(board,curmove):
                                moves.append(curmove)
        return moves

    def gobblet_exist(board: GameBoard, crow: int,ccol: int, palyer_type: str):
        """check if the gobblet at this position is able to move by player

        Args:
            board (GameBoard): current board
            crow (int): column of this gobblet
            ccol (int): row of this gobblet
            palyer_type (str): the current player

        Returns:
            able to move (bool): is there is free gobblet to move by me
        """
        return board.board[crow][ccol] == palyer_type
    
    @staticmethod
    def possiblePosition(board: GameBoard, curmove: move):
        """is this position is able to apply this move

        Args:
            board (GameBoard): current board
            curmove (move): the move to be abbly

        Returns:
            able to move (bool): is this position can be apply this move
        """
        return board.board[curmove.newRow][curmove.newCol] == ' '
    
    @staticmethod
    def Generate_nextBoard(currentBoatd : GameBoard, move: move):
        """generate the board after a move

        Args:
            currentBoatd (GameBoard): the current board before move
            move (move): the move to be do
        """
        board.board[move.curRow][move.curCol] = ' '
        board.board[move.newRow][move.newCol] = move.node
        
    @staticmethod
    def Undo(currentBoatd : GameBoard, move: move):
        """Undo this move from the board

        Args:
            currentBoatd (GameBoard): the current board after move
            move (move): the move to be undo
        """
        board.board[move.curRow][move.curCol] = move.node
        board.board[move.newRow][move.newCol] = ' '
        
    @staticmethod    
    def scoring(board: GameBoard):
        """get the score if the search get to final level without any winning or loss

        Args:
            board (GameBoard): the board to calculate the score for

        Returns:
            score (int): the score for this board
        """
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
        """        
        Performs the Alpha-Beta Pruning algorithm and returns the score of the board.

        Args:
            board (GameBoard): a list of lists representing the game board
            depth (int): the depth of the current node in the game tree
            max_depth (int): contain the maximum depth for search
            is_maximizing (bool): True if the current node is a maximizing node, False otherwise
            current_player (str): a string representing the current player which is either 'X' or 'O'

            alpha (float): the best value that the maximizing player can guarantee at the current level or above
            beta (float): the best value that the minimizing player can guarantee at the current level or above
            start_time (float): the time the search start at 
            time_limit (float): the duration the Search must not to be exceed 
        Returns:
            min_eval/max_val (int): the score of the board
            best_board (GameBoard): board after make move
            best_move (move); the move that it make
        """
        score = board.evaluate_board() 
        if score is not None:
            return score*100 / depth, board, None
        
        if depth == max_depth:
            return self.scoring(board) / depth, board, None
            # return 0,board, None
            if is_maximizing:
                return float('inf'),board, None
            else:
                return float('-inf'),board, None
        
        if is_maximizing:
            max_eval = float('-inf') #alpha
            best_board = GameBoard(grid_size=4) 
            best_board.board = copy.deepcopy(board.board)
            moves = self.get_nextMoves(self, board,current_player)
            best_move = None
            for move in moves:
                self.Generate_nextBoard(board, move)
                eval_score, temp_board,curmove = AIAlgorithms.alpha_beta_pruning(self, board, depth + 1, max_depth, False,'X' if current_player == 'O' else 'O',alpha, beta, start_time, time_limit )
                if(max_eval < eval_score):
                    max_eval = eval_score 
                    best_board.board = copy.deepcopy(board.board)
                    best_move = move
                self.Undo(board,move) # Undo the move

                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Beta cutoff
                
                if time.time() - start_time > time_limit:
                    # print(f"Time limit ({time_limit} seconds) exceeded. Terminating search.")
                    return max_eval, best_board, best_move

            return max_eval, best_board, best_move
        
        else:
            min_eval = float('inf')
            best_board = GameBoard(grid_size=4) 
            best_board.board = board.board.copy()
            best_move = None
            moves = self.get_nextMoves(self, board,current_player)
            for move in moves:
                self.Generate_nextBoard(board, move)
                eval_score, temp_board,curmove =  AIAlgorithms.alpha_beta_pruning(self, board, depth + 1, max_depth, True, 'X' if current_player == 'O' else 'O', alpha, beta, start_time, time_limit)
                
                if(min_eval > eval_score):
                    min_eval = eval_score 
                    best_board.board = copy.deepcopy(board.board)
                    best_move = move
                    
                self.Undo(board,move) # Undo the move
                
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Alpha cutoff
                
                if time.time() - start_time > time_limit:
                    # print(f"Time limit ({time_limit} seconds) exceeded. Terminating search.")
                    return min_eval, best_board, best_move

                if beta <= alpha:
                        break  # Alpha cutoff
            return min_eval, best_board, best_move
                    
    @staticmethod
    def get_best_move(self, board: GameBoard, is_max: bool, player: str, diffcult: int, time_limit:int=5):
        """get best moves in certain time and diffcult

        Args:
            board (GameBoard): current board before move
            is_max (bool): is this mixamizer or minimizer (X or O)
            player (str): the current player to play (X or O)
            diffcult (int): the level of diffculty (1 for easy, 2 for mediumm and 3 for hard)
            time_limit (int, optional): max time for cumputer play in this rount. Defaults to 5.

        Returns:
            min_eval/max_val (int): the score of the board
            best_board (GameBoard): board after make move
            best_move (move); the move that it make
        """
        start_time = time.time()
        depth = 1
        best_move = None
        t = time.time()
        if player == 'X':
            best_val = float('-inf')
        else:
            best_val = float('inf')
        if diffcult == 1:
            max_depth = 2
        elif diffcult == 2:
            max_depth = 4
        else:
            max_depth = 8    
        # max_depth = diffcult
        
        
        while time.time() - start_time < time_limit and depth <= max_depth:

            if best_move:
                print(f"Depth {depth - 1} completed in {time.time() - start_time:.2f} seconds")

            val, move, bestMove = self.alpha_beta_pruning(self, board, 0, depth, is_max, player, float('-inf'),float('inf'), t, time_limit)
            
            print("val: " + str(val) + ", best: " + str(best_val))
            print(move.board)
            if time.time() - start_time <= time_limit:
                print(f"Time inside decision: {time.time() - start_time:.2f} seconds")
                best_move = move
                best_val = val 
            depth += 1
        print(f"Interrupted Depth {depth - 1} completed in {time.time() - start_time:.2f} seconds")
        print("best: " + str(best_move.board))
        return best_val, best_move, bestMove

                
AI = AIAlgorithms

board = GameBoard(grid_size=4) 
bb = GameBoard(grid_size=4)
bb.board = copy.deepcopy(board.board)
board.board[0][0] = 'X'
board.board[1][0] = 'X'

board.board[0][1] = 'O'
board.board[1][1] = 'O'

board.board = [['X', ' ', ' ', ' '], 
               [' ', 'O', 'O', 'X'], 
               ['O', 'O', 'O', 'X'],
               [' ', 'X', ' ', 'X']]

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



# print(AI.scoring(board))
# mmx,board, bestMove= AI.alpha_beta_pruning(board, 4, True, 'X')

# moves = get_nextMoves(board,'X')
# for move in moves:
#     Generate_nextBoard(board, move)
#     Undo(board, move)


# mmx,board, bestMove= AI.get_best_move(AI,board,True, 'X',, 3, 5)
mmx,board, bestMove= AI.get_best_move(AI,board,False, 'O', 3, 15)
mmx,board, bestMove= AI.get_best_move(AI,board,True, 'X', 3, 15)
mmx,board, bestMove= AI.get_best_move(AI,board,False, 'O', 3, 15)
mmx,board, bestMove= AI.get_best_move(AI,board,True, 'X', 3, 15)
mmx,board, bestMove= AI.get_best_move(AI,board,False, 'O', 3, 15)
mmx,board, bestMove= AI.get_best_move(AI,board,True, 'X', 3, 15)
mmx,board, bestMove= AI.get_best_move(AI,board,False, 'O', 3, 15)
mmx,board, bestMove= AI.get_best_move(AI,board,True, 'X', 3, 15)
mmx,board, bestMove= AI.get_best_move(AI,board,False, 'O', 3, 5)
mmx,board, bestMove= AI.get_best_move(AI,board,True, 'X', 3, 5)
mmx,board, bestMove= AI.get_best_move(AI,board,False, 'O', 3, 5)

# # print(board.board)
mmo, board = AI.alpha_beta_pruning(AI, board,0,  4, True, 'X',float('-inf'),float('inf'))
# # print(board.board)
# mmx,board, bestMove= AI.alpha_beta_pruning(board, 0, True, 'X')
# # print(board.board)
# mmo, board = AI.alpha_beta_pruning(board, 0, False, 'O')
# # print(board.board)
# mmx,board, bestMove= AI.alpha_beta_pruning(board, 0, True, 'X')
# # print(board.board)
# mmo, board = AI.alpha_beta_pruning(board, 0, False, 'O')
# # print(board.board)
# mmx,board, bestMove= AI.alpha_beta_pruning(board, 0, True, 'X')
# # print(board.board)
# mmo, board = AI.alpha_beta_pruning(board, 0, False, 'O')
# # print(board.board)
# mmx,board, bestMove= AI.alpha_beta_pruning(board, 0, True, 'X')
# mmo, board = AI.alpha_beta_pruning(board, 0, False, 'O')
# mmx,board, bestMove= AI.alpha_beta_pruning(board, 0, True, 'X')
# mmo, board = AI.alpha_beta_pruning(board, 0, False, 'O')
# print(mmx)