# -*- coding: utf-8 -*-
"""
程式功能:
模擬「跳兔子」，
假設棋盤有150格，全部有7個金禮包，
用正常六面骰把棋盤格走完，
平均能跳到幾個金禮包?
"""

import random
from collections import defaultdict
def dice():
    return random.randrange(1,7)

golds = list(range(1,150))
random.shuffle(golds)
golds = golds[:7]

def ex():
    step, cnt = 0, 0
    while step< max(golds):
        roll = dice()
        step += roll
        if step in golds:
            cnt +=1
    return cnt

def simulate(experiment, times=100000):
    D = defaultdict(lambda: 0)
    for i in range(times):
        D[experiment()] += 1
    return D, sum(k*D[k] for k in D)/times

print(simulate(ex))