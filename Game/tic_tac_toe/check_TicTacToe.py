# 函數功能: 輸入井字遊戲的結束盤面，判斷是誰勝(平手返回'D')
# (保證不會有不合理的盤面)例: 
#  input:
# ["X.O", 
#  "XX.", 
#  "XOO"]
# output:
# "X"
def check_TicTacToe(board):
    rows = board
    cols = list(map(''.join, zip(*rows)))
    diags = list(map(''.join, zip(*[(r[i], r[2 - i]) for i, r in enumerate(rows)])))
    lines = rows + cols + diags

    if 'XXX' in lines:
        return 'X'  
    if 'OOO' in lines:
        return 'O' 
    return 'D'

board = ["X.O", "XX.", "XOO"]
print(check_TicTacToe(board))
