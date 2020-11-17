#from copy import deepcopy

import sys
sys.path.append('..') # 添加相對路徑上兩層到sys.path，讓程式找到的模組_package
from _package._game_theory.alpha_beta_algo import MinimaxABAgent
#
#class State():
#    """
#    記錄棋盤資訊，及下一步換誰下
#    """
#    def __init__(self, board, tile):
#        self.board = board
#        self.tile = tile  

class BitBoard():
    """
    用一個int表示棋盤狀態，
    tileNUm 表示有幾種棋子(usually = 2)，
    原以為做位元運算會非常快，
    實測當前速度極慢
    """
    def __init__(self, height, width, tileNum):
        self.width = width
        self.height = height
        self.tileNum = tileNum
        self.turn_bit = self.tileNum * self.width* self.height
#        self.helper =  {(x, y, i):x + y * width + i * width* height\
#                        for x in range(width) for y in range(height) for i in range(tileNum)}
        
    def isOnBoard(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height
    
    def _helper(self, x, y, tileIdx):
        if not self.isOnBoard(x, y) or tileIdx >= self.tileNum:
            #print(x,y,tileIdx)
            raise RuntimeError('Plase enter the valid x, y')
        return x + y * self.width + tileIdx * self.width* self.height
    
    def get_turn(self, state):
        # 回傳下一步棋換誰走
        return state >> self.turn_bit
        
    def get(self, state, x,y):
        for idx in range(self.tileNum):
            if (state >> self._helper(x,y, idx)) & 1:
                return idx
        return -1 # 座標x,y 上無棋子時回傳-1
    
    def set_xy(self, state, x,y, tileIdx):
        for idx in range(self.tileNum):
            state &= ~(1<<self._helper(x,y, idx)) 
        state |= (1<<self._helper(x,y, tileIdx))
        return state
    
    def opp_turn(self, state):
        return state ^ (1 << self.turn_bit)
    
    def to_board(self, state):
        """ For debug, 將state轉換回二維陣列 """
        board = [[-1]*self.width for _ in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                board[x][y] = self.get(state,x,y)        
        return board

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
        self.bitBoard = BitBoard(height, width, 2)
    
    def isOnBoard(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    #檢查tile放在某個座標是否為合法棋步，如果是則回傳翻轉的對手棋子
    """ ###################### """
    def isValidMove(self, state, tileIdx, xstart, ystart):
        if not self.isOnBoard(xstart, ystart) or self.bitBoard.get(state,xstart,ystart)!=-1:
            return False
        state = self.bitBoard.set_xy(state, xstart, ystart, tileIdx) # 暫時放置棋子
        otherTile = 1-tileIdx
        tilesToFlip = [] # 合法棋步
        dirs = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]] # 定義八個方向
        for xdir, ydir in dirs:
            x, y = xstart+xdir, ystart+ydir
            while self.isOnBoard(x, y) and self.bitBoard.get(state,x,y) == otherTile:
                x += xdir
                y += ydir
                # 夾到對手的棋子了，回頭記錄被翻轉的對手棋子
                if self.isOnBoard(x, y) and self.bitBoard.get(state,x,y) == tileIdx:
                    while True:
                        x -= xdir
                        y -= ydir
                        if x == xstart and y == ystart:
                            break
                        tilesToFlip.append([x, y])
                        
        if tilesToFlip:
            for x, y in tilesToFlip:
                state = self.bitBoard.set_xy(state, x,y, tileIdx)
            return self.bitBoard.opp_turn(state)
        return False

#
#    def makeMove(self, state, xstart, ystart):
#        board = deepcopy(state.board)
#        tilesToFlip = self.isValidMove(state.board, state.tile, xstart, ystart)
#        if tilesToFlip:
#            board[xstart][ystart] = state.tile
#            for x, y in tilesToFlip:
#                board[x][y] = state.tile
#        return State(board, 'O' if state.tile=='X' else 'X')


    def getValidMoves(self, state):
        moves = {(x, y):self.isValidMove(state, self.bitBoard.get_turn(state), x,y) for x in range(self.width) for y in range(self.height)}
        return {k:v for k,v in moves.items() if v}
    
    def evaluation_function(self, state, tile):
        # for 8*8 的計分
        score = 0
        opp = 1-tile
        for x in range(8):
            for y in range(8):
                if self.bitBoard.get(state,x,y) == tile:
                    score += weights[x][y]
                elif self.bitBoard.get(state,x,y) == opp:
                    score -= weights[x][y]    
        return score
    
    def is_terminal(self, state):
        if not self.getValidMoves(state):
            #state.tile = 'O' if state.tile=='X' else 'X'
            if not self.getValidMoves(self.bitBoard.opp_turn(state)):
                return True
        return False
    
#    # 計算當前比分
#    def getScoreOfBoard(self)-> dict:
#        scores = {'X':0, 'O':0}
#        for x in range(self.width):
#            for y in range(self.height):
#                tile = self.board[x][y]
#                if tile in scores:
#                    scores[tile] += 1
#        return scores

def board_to_state(board, tileIdx):
    height, width = len(board), len(board[0])
    bitBoard = BitBoard(height, width, 2)
    state = 0
    for y in range(height):
        for x in range(width):
            if board[x][y]=='X':
                state = bitBoard.set_xy(state, x,y, 0)
            elif board[x][y]=='O':
                state = bitBoard.set_xy(state, x,y, 1)
    return state
    
if __name__=='__main__':
    """
    黑白棋套用alpha-beta算法
    通過 https://www.hackerrank.com/challenges/reversi/problem 的測試
    目前計算上太慢，仍有許多改進空間
    """
    game = Reversi(8,8)
    AI = MinimaxABAgent(6, 0, game) #0 for 'X', 1 for 'O'
    board = [[' ',' ',' ', ' ', ' ', ' ', ' ', ' '],
             [' ',' ',' ', ' ', ' ', ' ', ' ', ' '],
             [' ',' ',' ', 'X', ' ', ' ', ' ', ' '],
             [' ',' ','O', 'O', 'O', 'O', ' ', ' '],
             [' ',' ',' ', 'X', 'O', ' ', ' ', ' '],
             [' ',' ',' ', ' ', ' ', ' ', ' ', ' '],
             [' ',' ',' ', ' ', ' ', ' ', ' ', ' '],
             [' ',' ',' ', ' ', ' ', ' ', ' ', ' ']]
    state = board_to_state(board, 0)
#    print(bin(state))
    bitBoard = BitBoard(8, 8, 2)
    #B = bitBoard.to_board(state)
    result = AI.choose_action(state)
    R = bitBoard.to_board(result[1])