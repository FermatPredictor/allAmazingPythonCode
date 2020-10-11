import random
character_num = 40
"""
程式功能: 
模擬抽卡包收集全套角色的期望次數，
其值依數學公式大約為n(1+1/2+...+1/n)
"""

def draw():
    return random.randint(1,character_num)

def ex():
    cnt = 0 #抽卡次數
    collections = set() # 目前你收集的角色集合
    while len(collections)< character_num:
        collections.add(draw())
        cnt += 1
    return cnt

def simulate(experiment, times=10000):
    cnt = 0
    for i in range(times):
        cnt += experiment()
    return cnt/times

print(simulate(ex))