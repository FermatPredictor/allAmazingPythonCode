"""
程式功能:
可以在任意不重複的5~7張牌中找出最大的牌型，
並能夠判斷兩副牌的大小。
"""
import time
from collections import Counter
from itertools import groupby

import sys
sys.path.append('..') # 添加相對路徑上層到sys.path，讓程式找到的模組_package
from _package._poker.poker_tool import Deck, StardardDeck

# 順子(注意A需要看作是1而非14)
def straight(rank):
    rank = sorted(set([1 if x==14 else x for x in rank]))
    for i in range(len(rank)-4):
        if rank[i+4]-rank[i]==4:
            return rank[i+4]
    return False
    
#回傳數字陣列恰好出現n次的數字，降序排列
def n_kind(rank, n):
    return sorted([k for k,v in Counter(rank).items() if v==n], reverse=True)


def card_rank(cards):
    """
    example: cards = ["5d", "5s", "9c", "9d", "9h"]
    輸出為 [9,9,9,5,5] 降序排列
    """
    return sorted(map(lambda s: '0123456789TJQKA'.index(s[0]), cards), reverse=True)


def groupby_suit(cards):
    """
    example: cards = ["5d", "5s", "9c", "9d", "9h"]
    group card by 花色，如{'c': [9], 'd': [9, 5], 'h': [9], 's': [5]}
    """
    cards = sorted(cards, key=lambda x:x[1])
    return {k:sorted(map(lambda c: '0123456789TJQKA'.index(c[0]), group), reverse=True) \
             for k,group in groupby(cards, lambda x:x[1])}


def hand_rank(hand):
    """
    hand 的格式為列表如 ["5d", "5s", "9c", "9d", "9h"] 來表示一手牌
    判斷手牌屬於何種牌型
    """
    rank = card_rank(hand)
    suit_gp = groupby_suit(hand)
    
    flush = sorted(filter(lambda v: len(v)>=5, suit_gp.values()), reverse=True)
    _straight = straight(rank)
    straightFlush = sorted(filter(lambda v: len(v)>=5 and straight(v), suit_gp.values()), reverse=True)
    
    single, pair, three_kind, four_kind = (n_kind(rank, i) for i in range(1,5))
    
    if straightFlush:
        return (9,max(straightFlush[0], key = lambda x: 1 if x==14 else x))
    if four_kind:
        head = four_kind[0]
        return (8,four_kind[0], max(filter(lambda r:r!=head,rank)))
    if len(three_kind)>=2 or three_kind and pair:
        head = three_kind[0]
        return (7,head, max(filter(lambda r:r!=head, pair+three_kind)))
    if flush:
        return (6, *flush[0][:5])
    if _straight:
        return (5, _straight)
    if three_kind:
        return (4,three_kind[0],*single[:2])
    if len(pair)>=2:
        return (3,*pair[:2],single[0])
    if len(pair)==1:
        return (2, pair[0],*single[:3])
    return (1,*single[:5])

#將一堆手牌按照牌型大小排序    
def pokerSort(hands):
    return sorted(hands,key=hand_rank,reverse=True)
                
if __name__=='__main__':
    
    deck = StardardDeck()
    hand = deck.rand_card(7)
    print(Deck(hand), hand_rank(hand))

    sf="2c 3c 3d 4d 4c 5c Ac"
    fk="Tc Td Th Ts 7c 7d 2c"
    fh="Tc Td Th 7c 7d 7s"
    f= "2d 5d 7d 9d Ad"
    s1="As 2s 3s 4s 5c"
    s2="2c 3c 4c 5c 6d"
    tk="3c 3d 3s 5d Ac"
    tp="5c 5d 9c 9d 6h"
    ah="As 2s 3s 4h 6d"
    sh="2d 3h 4h 6s 7d"
    hands=[sf,fk,fh,f,s1,s2,tk,tp,ah,sh]
    print(pokerSort([h.split() for h in hands]))
    for hand in hands:
        print(hand, hand_rank(hand.split()))
    
    """
    用程試測試隨機五張牌的牌型概率，與數學算出來的理論值比較
    各牌型的出現概率如下:
    
    straight flush    0.0014%
    four of a kind    0.0240%
    full house        0.1441%
    flush             0.1965%
    straight          0.3925%
    three of a kind   2.1128%
    two pair          4.7539%
    one pair          42.2569%
    high card         50.1177%
    
    五~七張牌的機率: https://home.gamer.com.tw/creationDetail.php?sn=3828045
    
    實測一百萬次隨機取五張牌，大致與理論值接近:
    Total time= 28.431500 seconds
    #由高牌到同花順的出現次數
    [501392, 421984, 47823, 21211, 3953, 1994, 1406, 222, 15]
    
    [TODO] 目前判斷牌型太花時間，需調整
    """
    List=[0]*9
    tStart = time.time()#計時開始
    deck = StardardDeck()
    for _ in range(10000):
        cardType=hand_rank(deck.rand_card(5))[0]
        List[cardType-1]+=1
    tEnd = time.time()#計時結束
    print("Total time= %f seconds" % (tEnd - tStart))
    print(List)
