from copy import deepcopy

import sys
sys.path.append('..') # 添加相對路徑上兩層到sys.path，讓程式找到的模組_package
from _package._game_theory.alpha_beta_algo import MinimaxABAgent

class State():
    """
    記錄棋盤資訊，及下一步換誰下
    """
    def __init__(self, board, tile):
        self.board = board
        self.tile = tile  

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

    #檢查tile放在某個座標是否為合法棋步，如果是則回傳被翻轉的棋子
    def isValidMove(self, board, tile, xstart, ystart):
        if not self.isOnBoard(xstart, ystart) or board[xstart][ystart]!=' ':
            return []
        board[xstart][ystart] = tile # 暫時放置棋子
        otherTile = 'O'  if tile == 'X' else 'X'
        tilesToFlip = [] # 合法棋步
        dirs = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]] # 定義八個方向
        for xdir, ydir in dirs:
            x, y = xstart+xdir, ystart+ydir
            while self.isOnBoard(x, y) and board[x][y] == otherTile:
                x += xdir
                y += ydir
                # 夾到對手的棋子了，回頭記錄被翻轉的對手棋子
                if self.isOnBoard(x, y) and board[x][y] == tile:
                    while True:
                        x -= xdir
                        y -= ydir
                        if x == xstart and y == ystart:
                            break
                        tilesToFlip.append([x, y])
                        
        board[xstart][ystart] = ' ' # 重設為空白
        return tilesToFlip


    def makeMove(self, state, xstart, ystart):
        board = deepcopy(state.board)
        tilesToFlip = self.isValidMove(state.board, state.tile, xstart, ystart)
        if tilesToFlip:
            board[xstart][ystart] = state.tile
            for x, y in tilesToFlip:
                board[x][y] = state.tile
        return State(board, 'O' if state.tile=='X' else 'X')


    def getValidMoves(self, state):
        return {(x, y):self.makeMove(state, x,y) for x in range(self.width) for y in range(self.height)
                if self.isValidMove(state.board, state.tile, x, y)}
    
    def evaluation_function(self, state, tile):
        # for 8*8 的計分
        score = 0
        opp = 'O' if tile=='X' else 'X'
        for x in range(8):
            for y in range(8):
                if state.board[x][y] == tile:
                    score += weights[x][y]
                elif state.board[x][y] == opp:
                    score -= weights[x][y]    
        return score
    
    def is_terminal(self, state):
        if not self.getValidMoves(state):
            state.tile = 'O' if state.tile=='X' else 'X'
            if not self.getValidMoves(state):
                return True
        return False
    
    # 計算當前比分
    def getScoreOfBoard(self)-> dict:
        scores = {'X':0, 'O':0}
        for x in range(self.width):
            for y in range(self.height):
                tile = self.board[x][y]
                if tile in scores:
                    scores[tile] += 1
        return scores


if __name__=='__main__':
    """
    黑白棋套用alpha-beta算法
    通過 https://www.hackerrank.com/challenges/reversi/problem 的測試
    但目前由於創建太多state物件，
    deepcopy太多board，
    感覺計算上太慢，仍有許多改進空間
    """
    game = Reversi(8,8)
    AI = MinimaxABAgent(4, 'X', game)
    board = [[' ',' ',' ', ' ', ' ', ' ', ' ', ' '],
             [' ',' ',' ', ' ', ' ', ' ', ' ', ' '],
             [' ',' ',' ', 'X', ' ', ' ', ' ', ' '],
             [' ',' ','O', 'O', 'O', 'O', ' ', ' '],
             [' ',' ',' ', 'X', 'O', ' ', ' ', ' '],
             [' ',' ',' ', ' ', ' ', ' ', ' ', ' '],
             [' ',' ',' ', ' ', ' ', ' ', ' ', ' '],
             [' ',' ',' ', ' ', ' ', ' ', ' ', ' ']]
    state = State(board, 'X')
    result = AI.choose_action(state)