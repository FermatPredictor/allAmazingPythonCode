"""
程式功能: 給定一個9*9數獨(空格為'.')
1. 可以判斷數獨是否合法(合法未必有解)
2. 暴力搜索嘗試找到一組可能的解
"""

from itertools import product
from typing import List
from pprint import pprint
import time

class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        row = [list(filter(lambda x: x!='.', y)) for y in board]
        col = [list(filter(lambda x: x!='.', y)) for y in zip(*board)]
        block = [[board[i+m][j+n] for m in range(3) for n in range(3) if board[i+m][j+n] != '.'] \
                  for i in range(0, 9, 3) for j in range(0, 9, 3)]
        return all(len(set(x)) == len(x) for x in (*row, *col, *block))
    
    def solveSudoku(self, board: List[List[str]]) -> None:
        def isValid(x,y, num):
            col = [board[i][y] for i in range(9)]
            row = [board[x][i] for i in range(9)]
            block = [board[x//3*3+i][y//3*3+j] for i in range(3) for j in range(3)]
            return num not in col+row+block
        
        def dfs(board):
            for i, j in product(range(9), range(9)):
                if board[i][j]=='.':
                    for k in filter(lambda n: isValid(i,j,n),'123456789'):
                        board[i][j]=k
                        if dfs(board):
                            return True
                        board[i][j]='.'
                    return False
            return True
        dfs(board)
        
def sepList(L,step):
    return [L[i:i+step] for i in range(0,len(L),step)]

sudoku= (
'53..7....'
'6..195...'
'.98....6.'
'8...6...3'
'4..8.3..1'
'7...2...6'
'.6....28.'
'...419..5'
'....8..79')

solver = Solution()
sudoku =[list(s) for s in sepList(sudoku,9)]
tStart = time.time()
solver.solveSudoku(sudoku)
pprint(sudoku)
print(f"Total time= {time.time()-tStart:.3f} seconds")