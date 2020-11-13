from copy import deepcopy

import sys
sys.path.append('..') # 添加相對路徑上兩層到sys.path，讓程式找到的模組_package
from _package._game_theory.alpha_beta_algo import MinimaxABAgent

class State():
    def __init__(self, board, tile):
        self.board = board
        self.tile = tile   


# 寫井字遊戲的基本邏輯，棋子共'X','O'兩種
class TicTacToe():
    def __init__(self):
        pass
    
    def isOnBoard(self, x, y):
        return 0 <= x < 3 and 0 <= y < 3
        
    #檢查tile放在某個座標是否為合法棋步
    def isValidMove(self, state, x, y):
        return self.isOnBoard(x, y) and state.board[x][y]==' '

    # 把棋子下在座標x, y的地方
    def makeMove(self, state, x, y):
        board = deepcopy(state.board)
        if self.isValidMove(state, x, y):
            board[x][y]=state.tile
        return State(board, 'O' if state.tile=='X' else 'X')
    
    # 回傳現在盤面輪到tile走的所有合法棋步
    def getValidMoves(self, state):
        return {(x, y):self.makeMove(state, x,y) for x in range(3) for y in range(3) if self.isValidMove(state, x, y)}

    # 判斷一個盤面是否有人贏了
    def check_TicTacToe(self, state):
        rows = list(map(''.join,state.board))
        cols = list(map(''.join, zip(*rows)))
        diags = list(map(''.join, zip(*[(r[i], r[2 - i]) for i, r in enumerate(rows)])))
        lines = rows + cols + diags
    
        if 'XXX' in lines:
            return 'X'  
        if 'OOO' in lines:
            return 'O' 
        return 'D' # draw(和棋)
    
    def evaluation_function(self, state, tile):
        if not self.is_terminal(state):
            return 0
        winner = self.check_TicTacToe(state)
        if winner == tile:
            return 100
        if winner == 'D':
            return 0
        return -100
    
    def is_terminal(self, state):
        if self.check_TicTacToe(state) in ('X','O'):
            return True
        for i in range(3):
            for j in range(3):
                if state.board[i][j]==' ':
                    return False
        return True
    
    
if __name__=='__main__':
    """
    井字棋套用alpha-beta算法
    通過 https://www.hackerrank.com/challenges/tic-tac-toe/problem 的測試
    """
    game = TicTacToe()
    AI = MinimaxABAgent(8, 'X', game)
    board = [[' ',' ','O'],
             [' ',' ',' '],
             [' ',' ',' ']]
    state = State(board, 'X')
    result = AI.choose_action(state)