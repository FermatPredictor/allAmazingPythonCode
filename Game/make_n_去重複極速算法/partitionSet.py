# -*- coding: utf-8 -*-
from pprint import pprint # 用pprint可以美化輸出格式

# 窮舉分割集合成多個子集合的所有可能
def enumAllPartitionCode(n):
    if n==1: 
        return [[0]]
    return [p+[i] for p in enumAllPartitionCode(n-1) for i in range(max(p)+2)]

# 給定m，窮舉分割集合成恰好m個子集合的所有可能
def enumPartCode(n, m):
    if n==0 or m==0 or m>n:
        return []
    if m==1:
        return [[0]*n]
    if n==m:
        return [list(range(n))]
    return [p+[i] for p in enumPartCode(n-1, m) for i in range(m)]+\
           [p+[m-1] for p in enumPartCode(n-1, m-1)]

# 編碼轉分割方式，如arr是['A', 'B', 'C']，
# partCode是[0,1,0]，則分割方式為 [['A', 'C'], ['B']]
def codeToSet(arr, partCode):
    L=[[] for i in range(max(partCode)+1)]
    for i,e in enumerate(partCode):
        L[e].append(arr[i])
    return tuple(map(tuple,sorted(L)))


#第二個參數表示要把集合分成幾個子集，不寫則列出全部分法
def enumPatitionSet(arr, m=None):
    arr = sorted(arr) #先保證input排序過
    partCodes = enumAllPartitionCode(len(arr)) if m==None else enumPartCode(len(arr),m)
    return set(codeToSet(arr,p) for p in partCodes)
    
if __name__=='__main__':
    pprint(enumAllPartitionCode(3))
    pprint(enumPatitionSet('ACC'))
    pprint(enumPatitionSet('ABCD',2))
    pprint(enumPatitionSet('AABB',2))