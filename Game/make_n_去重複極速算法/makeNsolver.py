# makeNsolver.py
from anytree import Node, RenderTree
from itertools import product
import copy
import time
import partitionSet as ps

# Operators 
OP_ADD = 1  # Addition 
OP_SUB = 2  # Subtraction 
OP_MUL = 3  # Multiplication 
OP_DIV = 4  # Divition
OP_INVDIV = 5

ops=[OP_ADD,OP_SUB,OP_MUL,OP_DIV,OP_INVDIV]


#窮舉所有可能的樹形(只用數字分兩個集合產生的樹形，沒有掛運算子)
def enumCalcTree(numArr):
    if len(numArr)==1:
        return [Node(numArr[0])]
    res = []
    for Left, Right in ps.enumPatitionSet(numArr, m=2):
        for treePair in product(enumCalcTree(Left), enumCalcTree(Right)):
            u = Node('[]')
            for p in treePair:
                temp_tree = copy.copy(p) #應先複製一份接再parent, 直接寫p.parent = u 好像會錯(待檢查或思考更清楚)
                temp_tree.parent = u
            res.append(u)
    return res
                
def opFunc(a,b,op):
    ops = {OP_ADD: lambda a,b: a+b,
           OP_SUB: lambda a,b: abs(a-b),
           OP_MUL: lambda a,b: a*b,
           OP_DIV: lambda a,b: a/b,
           OP_INVDIV: lambda a,b: b/a}
    #排除可能碰到除以0的例外
    try:
        return ops[op](a,b)
    except:
        return None


def strOpFunc(list1,list2,op):
    
    # input兩數字及運算子，回傳字串表示法
    def strExp(a,b,op_symbol):
        return "("+str(a)+op_symbol+str(b)+ ")"
    
    if op==OP_ADD: 
        return strExp(list1[0], list2[0],'+')
    if op==OP_SUB:
        try:
            return strExp(list1[0], list2[0],'-') if list1[1]>list2[1] else strExp(list2[0], list1[0],'-')
        except:
            return None
    if op==OP_MUL: 
        return strExp(list1[0], list2[0],'*')
    if op==OP_DIV: 
        return strExp(list1[0], list2[0],'/')
    if op==OP_INVDIV: 
        return strExp(list2[0], list1[0],'/')
    

"""
考慮「交換律」、「結合律」的特性，減少計算很多case
(交換律在把數字分兩堆產生樹形時就會避免左、右對調的重複)
1. (結合律)我們可以限定「加」、「乘」的左子樹都不可以跟該節點相同。
proof: (A+B)+(anyTree)=A+(B+anyTree)

2. 我們可以限定「加」、「減」的子樹都不可以是「減號」;「乘」、「除」的子樹都不可以是「除號」。
proof: (A-B)+(anyTree)=(A+anyTree)-B
若「加」、「減」的子樹為「減號」時，取父節點為「減號」的樹做代表即可。
"""
def opRule(leftop, rightop, rootop):
    if rootop in [OP_ADD,OP_MUL]:
        if leftop==rootop:
            return False
    if rootop in [OP_ADD,OP_SUB]:
        if leftop==OP_SUB or rightop==OP_SUB:
            return False
    if rootop in [OP_MUL,OP_DIV,OP_INVDIV]:
        if leftop in [OP_DIV,OP_INVDIV] or rightop in [OP_DIV,OP_INVDIV]:
            return False
    return True

# 計算左子樹與右子樹搭配運算子所能產生的所有運算式與運算結果
def tree_combination(tree1,tree2):
    return [[strOpFunc(T1,T2,op), opFunc(T1[1],T2[1],op),op] for T1 in tree1 for T2 in tree2\
             for op in ops if opRule(T1[2],T2[2],op)]


#記錄這個樹形能夠產生的所有運算式與運算結果    
def evalTree(tree):
    if tree.is_leaf:
        return [[str(tree.name), int(tree.name),None]]
    return tree_combination(evalTree(tree.children[0]),evalTree(tree.children[1]))

#印出所有算式解
def makeNsolver(nums, targetNum):
    """
    函數功能:
    input: nums(數字陣列), targetNum(數字)，
    印出所有nums的數字能湊出targetNum的算式解
    因為浮點數計算有誤差，應定義合理誤差範圍
    
    每找到一組解就印出。
    """
    err = 10**(-6)
    for tree in enumCalcTree(nums):
        for p in evalTree(tree):
            try:
                if abs(p[1]-targetNum)<err:
                    print(str(targetNum) + "=" +p[0])
            except Exception:
                pass

if __name__ == '__main__':
    nums, targetNum = [4,5,6,9,8,20], 1005

    #打開註解印出所有樹
#    tStart = time.time()#計時開始
#    count=0
#    for tree in enumCalcTree(nums):
#        count=count+1
#        for pre, fill, node in RenderTree(tree):
#            print("%s%s" % (pre, node.name))
#    print(count)
#    tEnd = time.time()#計時結束
#    print(tEnd - tStart)
 
    
    #印出所有解
    tStart = time.time()#計時開始
    makeNsolver(nums, targetNum)
    tEnd = time.time()#計時結束
    print(f'Total time is {tEnd - tStart} seconds')