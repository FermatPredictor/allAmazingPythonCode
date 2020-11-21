import time
import random
from pprint import pprint

class State():
    """ 
    記錄棋盤資訊，及下一步換誰下
    player_color : int(usually 1 or 2, 0 for empty grid)
    """
    def __init__(self, board, playerColor):
        self.board = board
        self.playerColor = playerColor
    
    def opp_color(self):
        return 3^self.playerColor

# the weights of board, big positive value means top priority for opponent
weights = [[ 100, -20,  10,   5,   5,  10, -20, 100],
           [ -20, -50,  -2,  -2,  -2,  -2, -50, -20],
           [  10,  -2,   1,   1,   1,   1,  -2,  10],
           [   5,  -2,   1,   1,   1,   1,  -2,   5],
           [   5,  -2,   1,   1,   1,   1,  -2,   5],
           [  10,  -2,   1,   1,   1,   1,  -2,  10],
           [ -20, -50,  -2,  -2,  -2,  -2, -50, -20],
           [ 100, -20,  10,   5,   5,  10, -20, 100]]

# 寫黑白棋遊戲的基本邏輯，棋子共'X','O'兩種
class Reversi():
    def __init__(self, height, width):
        self.width = width
        self.height = height
    
    def isOnBoard(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    #檢查tile放在某個座標是否為合法棋步，如果是則回傳翻轉的對手棋子
    def isValidMove(self, state, xstart, ystart):
        if not self.isOnBoard(xstart, ystart) or state.board[xstart][ystart]!=0:
            return False
        tile, opp_tile = state.playerColor , state.opp_color()
        tilesToFlip = [] # 合法棋步
        dirs = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]] # 定義八個方向
        for xdir, ydir in dirs:
            x, y = xstart+xdir, ystart+ydir
            while self.isOnBoard(x, y) and state.board[x][y] == opp_tile:
                x, y = x+xdir, y+ydir
                # 夾到對手的棋子了，回頭記錄被翻轉的對手棋子
                if self.isOnBoard(x, y) and state.board[x][y] == tile:
                    x, y = x-xdir, y-ydir
                    while not (x == xstart and y == ystart):
                        tilesToFlip.append([x, y])
                        x, y = x-xdir, y-ydir
        if tilesToFlip:
            return [[xstart, ystart]] + tilesToFlip
        return False


    def makeMove(self, state, action_key):
        for x, y in action_key:
            state.board[x][y] = state.playerColor
        state.playerColor = state.opp_color()
            
    def unMakeMove(self, state, action_key):
        place_x, place_y = action_key[0]
        state.board[place_x][place_y] = 0
        for x, y in action_key[1:]:
            state.board[x][y] = state.playerColor
        state.playerColor = state.opp_color()


    def getValidMoves(self, state):
        moves = {(x, y):self.isValidMove(state, x,y) for x in range(self.width) for y in range(self.height)}
        return {k:v for k,v in moves.items() if v}
    
    def evaluation_function(self, state, tile):
        # for 8*8 的計分
        score = 0
        opp = 3-tile
        for x in range(8):
            for y in range(8):
                if state.board[x][y] == tile:
                    score += weights[x][y]
                elif state.board[x][y] == opp:
                    score -= weights[x][y]    
        return score
    
    def is_terminal(self, state):
        if not self.getValidMoves(state):
            state.playerColor = state.opp_color()
            if not self.getValidMoves(state):
                state.playerColor = state.opp_color()
                return True
            state.playerColor = state.opp_color()
        return False

""" ref: https://www.mygreatlearning.com/blog/alpha-beta-pruning-in-ai/ """
class MinimaxABAgent:
    """
    alpha beta 演算法模版，
    用途是只要定義好遊戲規則，
    ai就會透過此演算法計算最佳行動(棋步)
    
    必要定義的物件:
    * state
    * game
       - def getValidMoves(self, state): 回傳一個字典，key值是行動，value是抵達的state
       - def evaluation_function(self, state, player_color): 回傳此盤面對「player_color」來說的分數，盤面愈好分數愈高
       - def is_terminal(self, state): 判斷一場遊戲是否已經結束
    """
    
    def __init__(self, max_depth, player_color, game, state):
        """
        Initiation
        Parameters
        ----------
        max_depth : int
            The max depth of the tree
        player_color : int(usually 1 or 2, 0 for empty grid)
            The player's index as MAX in minimax algorithm
        """
        self.max_depth = max_depth
        self.player_color = player_color
        self.game = game
        self.state = state
        self.node_expanded = 0
 
    def choose_action(self):
        """ 回傳(行動, state) """
        self.node_expanded = 0
 
        start_time = time.time()
 
        print("MINIMAX AB : Wait AI is choosing")
        list_action = self.game.getValidMoves(self.state)
        eval_score, selected_key_action = self._minimax(0,state,True,float('-inf'),float('inf'))
        print(f"MINIMAX : Done, eval = {eval_score}, expanded {self.node_expanded} nodes")
        eval_time = time.time() - start_time
        print(f"--- {eval_time} seconds ---, avg: {self.node_expanded/eval_time} (explode_node per seconds)")
        self.game.makeMove(self.state, list_action[selected_key_action])
        return (selected_key_action, self.state)
 
    def _minimax(self, current_depth, state, is_max_turn, alpha, beta):
        
        self.node_expanded += 1
 
        if current_depth == self.max_depth or self.game.is_terminal(state):
            return self.game.evaluation_function(state, self.player_color), ""
 
        possible_action = self.game.getValidMoves(state)
        key_of_actions = list(possible_action.keys())
 
        random.shuffle(key_of_actions) #randomness
        best_value = float('-inf') if is_max_turn else float('inf')
        action_target = ""
        for action_key in key_of_actions:
            self.game.makeMove(state, possible_action[action_key])
 
            eval_child, action_child = self._minimax(current_depth+1,state, not is_max_turn, alpha, beta)
            
            max_condition = is_max_turn and best_value < eval_child
            min_condition = (not is_max_turn) and best_value > eval_child
            
            if max_condition or min_condition:
                best_value = eval_child
                action_target = action_key
                
                if max_condition:
                    alpha = max(alpha, best_value)
                else:
                    beta = min(beta, best_value)
                    
                if beta <= alpha:
                    self.game.unMakeMove(state, possible_action[action_key])
                    break
            
            self.game.unMakeMove(state, possible_action[action_key])
 
        return best_value, action_target
    
if __name__=='__main__':
    """
    黑白棋套用alpha-beta算法
    通過 https://www.hackerrank.com/challenges/reversi/problem 的測試
    但目前由於創建太多state物件，
    deepcopy太多board，
    感覺計算上太慢，仍有許多改進空間
    """
    board = [[0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,1,0,0,0,0],
             [0,0,2,2,2,2,0,0],
             [0,0,0,1,2,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0]]
    state = State(board, 1)
    game = Reversi(8,8)
    AI = MinimaxABAgent(7, 1, game, state)
    result = AI.choose_action()