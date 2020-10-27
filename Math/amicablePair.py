"""
<說明>
我們稱一對整數a,b是相親數若
a自身外的正因數和 = b 且 b自身外的正因數和 = a
例:
220的所有因子：1+2+4+5+10+11+20+22+44+55+110 = 284
284的所有因子：1+2+4+71+142 = 220
(220,284)為一對相親數(或友好數)(amicable pair)

本支程式首先判斷一個數是否是完全數，
不是的話嘗試找是否有相親數對

<延伸>
若a除了自身與1之外的正因數和 = b 且 b除了自身與1之外的正因數和 = a
則a,b稱為婚約數(betrothed numbers)，如(48,75)
驚人的性質為:
目前發現的友好數全是同奇同偶的關係，
而婚約數全是一奇一偶的關係。
"""

# divisorsum的簡寫
def DS(n):
    return sum([sum({i,n//i}) for i in range(1,int(n**0.5)+1) if n%i==0])-n

while True:
    n = int(input())
    if n==0:
        break
    divisorSum = DS(n)
    if divisorSum == n:
        print(f"={n}") #完全數
    else:
        print(divisorSum if DS(divisorSum)==n else 0) #判斷有沒有友好數對
