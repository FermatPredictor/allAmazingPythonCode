import time
import random

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
       - def evaluation_function(self, state, player_color): 回傳此盤面對「 player_color」來說的分數，盤面愈好分數愈高
       - def is_terminal(self, state): 判斷一場遊戲是否已經結束
    """
    
    def __init__(self, max_depth, player_color, game):
        """
        Initiation
        Parameters
        ----------
        max_depth : int
            The max depth of the tree
        player_color : int
            The player's index as MAX in minimax algorithm
        """
        self.max_depth = max_depth
        self.player_color = player_color
        self.game = game
        self.node_expanded = 0
 
    def choose_action(self, state):
        """ 回傳(行動, state) """
        self.node_expanded = 0
 
        start_time = time.time()
 
        print("MINIMAX AB : Wait AI is choosing")
        list_action = self.game.getValidMoves(state)
        eval_score, selected_key_action = self._minimax(0,state,True,float('-inf'),float('inf'))
        print(f"MINIMAX : Done, eval = {eval_score}, expanded {self.node_expanded}")
        print("--- %s seconds ---" % (time.time() - start_time))
        return (selected_key_action,list_action[selected_key_action])
 
    def _minimax(self, current_depth, state, is_max_turn, alpha, beta):
 
        if current_depth == self.max_depth or self.game.is_terminal(state):
            return self.game.evaluation_function(state, self.player_color), ""
 
        self.node_expanded += 1
 
        possible_action = self.game.getValidMoves(state)
        key_of_actions = list(possible_action.keys())
 
        random.shuffle(key_of_actions) #randomness
        best_value = float('-inf') if is_max_turn else float('inf')
        action_target = ""
        for action_key in key_of_actions:
            new_state = possible_action[action_key]
 
            eval_child, action_child = self._minimax(current_depth+1,new_state,not is_max_turn, alpha, beta)
            
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
                    break
 
        return best_value, action_target