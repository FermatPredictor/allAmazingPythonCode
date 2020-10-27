"""
函數功能: 檢查陣列Set裡面(元素可重複)是否有子集合的和 = Sum
注意sum = 0 時答案為 True
解法說明:
python 的特化解法，DP是一個bit_vector，
其中從右往左數第i個位數，代表目前為止的Set的元素是否子集和= Sum
譬如說 Set = [2,2,3,5]
一開始DP = 1，
更新一輪之後就變成 1 | 101 = 101(二進位來看)，
再更新一輪之後變成 10100 | 101 = 10101，
解讀為[2,2]可以湊出子集和 = 0, 2, 4
由於python沒有像c++的int有溢位問題，
程式寫起來特簡單
"""
def isSubsetSum(Set,Sum): 
    DP = 1 
    for e in Set:
        DP = DP | (DP << e)
    return DP & (1 << Sum) != 0

"""
基礎程式功能: 給定一個正整數，把它所有的可能總和分解列出來
例: N=3。
3=1+1+1=1+2=3
Output:
[1, 1, 1]
[1, 2]
[3]

必選參數:
n: 被分割的正整數

可選參數:
m: 只能使用大於等於m的數
M: 只能使用小於等於M的數(預設9999)
part: 分解n的總和至少part個
most_part: 分解n的總和不超過part個
avoidList: 不可以用avoidList的數
avoidSum: 任何子集合不可以等於avoidSum裡的數
"""
def partitions(n, m=1,M=9999, part=1, most_part = 9999, avoidList=(), avoidSum=()):
	# 終止條件: 0是空list的總和
    if n == 0:
        return [[]]
    # 終止條件: 若最多只能再切割一塊，回傳n
    if n>=m and n<=M and most_part == 1:
        return [[n]]
    parts = []
    for i in range(m,min(M+1,n+2-part)):
        if i not in avoidList:
            for p in partitions(n-i, i,M, max(1,part-1), most_part-1, avoidList, avoidSum):
                if all([not isSubsetSum([i]+p, s) for s in avoidSum]):
                    parts.append([i] + p)
    return parts

# 測試函數
def testPartitions(n, m=1,M=9999, part=1, most_part = 9999, avoidList=(), avoidSum=()):
    print(f"分割整數{n}")
    print(f"最小可用的數字為{m}, 最大可用的數字為{M}")
    print(f"最少需切成{part}個part, 最多需切成{most_part}個part")
    if avoidList:
        print(f'不可以用{avoidList}的數')
    if avoidSum:
        print(f'任何子集合不可以等於{avoidSum}裡的數')
    parts = partitions(n,m,M, part, most_part, avoidList, avoidSum)
    print(f"分解方法數共{len(parts)}種，具體方法:")
    for p in parts:
        print(p)
    print()



if __name__=='__main__':
    testPartitions(6)
    testPartitions(6, part=3, most_part = 3)
    testPartitions(6, avoidList=[3,4])
    testPartitions(8, avoidSum=[3])
    testPartitions(8, part=3)
    testPartitions(6, m=1, part=2, avoidList=[3,4])
