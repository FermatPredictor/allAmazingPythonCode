# -*- coding: utf-8 -*-
"""
問題: 我們有很多個硬幣，至少一個是公正硬幣，
其它硬幣出現正面的機率可能在0~1之間，
那麼要如果用這堆硬幣模擬一個公正硬幣呢?

<解> 用程式計算的結果，把出現正面次數為偶數的結果加起來大概就是0.5
<證明> 用數學歸納法。一個公正硬幣可以跟不公正硬幣合體變成一個公正硬幣，
從而可以從k推到k+1
"""

import random
P=[0.5]+[round(random.random(),1) for i in range(7)]
print("每個銅板丟出正面的機率分別為:",P)

# 這個函數來自LeetCode1230題(lock)
# prob計錄著每個硬幣丟出正面的機率，回傳恰好丟出target個硬幣是正面的機率
# DP解，令dp[k]表示丟出k個正面的機率
# Time = O(N^2), Space= O(N)
# 想法: 每次加入一個硬幣，要丟出k個硬幣，可能是丟出k-1個硬幣正面接著新硬幣正面或丟出k-1個硬幣正面接著新硬幣反面
def probOfHeads(prob, target):
    dp = [1] + [0] * target #初始值: 0個硬幣、100%0個硬幣正面
    for p in prob:
        for k in range(target, -1, -1):
            dp[k] = (dp[k - 1] if k>0 else 0) * p + dp[k] * (1 - p)
    return dp[target]


headProb=[round(probOfHeads(P,i),6) for i in range(len(P)+1)]

for (i,e) in enumerate(headProb):
    print(f'出現{i}個正面的機率為{e}')
print(f'出現偶數個正面的機率為{sum(headProb[::2])}')