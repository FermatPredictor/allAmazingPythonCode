"""
題設:
老師告訴S, P兩個人 1< x<y 且 x+y<=ubd(ubd是一個給定的常數，upper bound的意思)，
然後老師說給S「x+y」的結果，
給P「xy」的結果。
然後有了以下一段對話:
P: 我不知道x,y
S: 我本來就知道你不知道
P: 那我知道了
S: 那我也知道了

那麼可能的x,y是多少?
實測: 若ubd<=64時無解，
ubd=65時有唯一解(4, 13)，
到ubd=1685時有第二組解(4, 61)
"""

ubd = 1685

# 所有可能的乘積分解，需滿足1< x<y 且 x+y<=ubd的條件
def prod_divide(n):
    return [(i,n//i) for i in range(2,int(n**0.5)+1) if n%i==0 and i!=n//i and i+n//i<=ubd]

# 所有可能的總和分解，需滿足1<x<y的條件
def sum_divide(n):
    return [(i,n-i) for i in range(2,n//2)]

# 檢查錯誤的函數，說明在第二句話「我本來就知道你不知道」的時機，若S的數不可能是n，是因為哪種分解使得P可能會知道x,y
def debug1(n):
    for a,b in sum_divide(n):
        if len(prod_divide(a*b))==1:
            print(a,b)


# 檢查若S拿到數字n(至少大於5)，能否說出「我本來就知道你不知道」
# 亦即對於n的所有總和分解，它們的積存在兩組以上的乘法分解，並且相加小於ubd
# 首先，S的數字至少要大於5，然後再滿足上述條件
def check2(n):
    return n>5 and all(len(prod_divide(a*b))>1 for a,b in sum_divide(n))

# 檢查若P拿到數字n，能否說出「那我知道了」
# 即是否n恰有一組乘積分解的和落在S講出「我本來就知道你不知道」的集合裡)
def check3(n, S):
    return sum(a+b in S for a,b in prod_divide(n))==1

"""
【函數功能】: 嘗試找出滿足對話的S、P可能拿到的數。
從S的立場來看，對於S拿到的數n，考慮n的所有總和分解，
計算其乘積然後代入P的角度看看P有沒有辦法知道。
對於P來說，P那個數的乘法分解的和只能有一組落在S的可能裡，
P才會說出「那我知道了」
然後，如果只有一種總和分解的可能使P會說出「那我知道了」，
那麼 S就可以確定兩數和與兩數積，進而說出「那我也知道了」
"""
def findXY(S):
    for s in S:
        possible=[]
        for a,b in sum_divide(s):
            if check3(a*b, S):
                possible.append((a,b))
            if len(possible)>1:
                break
        if len(possible)<=1:
            print(s, possible)


if __name__ == "__main__":
    S = [i for i in range(ubd) if check2(i)]
    print(S)
    findXY(S)
