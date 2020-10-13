"""
程式功能:
可以在任意不重複的5~7張牌中找出最大的牌型，
並能夠判斷兩副牌的大小。
"""

import random
from collections import Counter

class Card():
    def __init__(self, cardStr, symbol):
        self.cardStr = cardStr
        self.symbol = symbol
        self.showing=False
    def __repr__(self):
        if self.showing:
            return self.symbol
        else:
            return "Card"
 
#用一字串表示一張牌，比如說梅花10是Tc，紅心A是Ah
def strToCard(cardStr):
    suits = {"h":"♡", "s":"♠", "d":"♢", "c":"♣"}
    symbol = cardStr[0]+suits[cardStr[1]]
    return Card(cardStr,symbol)
       
class Deck():  
    def shuffule(self, time=1):
        random.shuffle(self.cards)
        print("Deck shuffled")
        
    def deal(self):
        return self.cards.pop(0)
    
    #放幾張特定的牌進牌堆，字串格式如 "5d 5s 9c 9d 9h"
    def put(self, cardStr):
        self.cards += list(map(strToCard, cardStr.split()))
    
    #抽出一張指定的牌
    def draw(self, cardStr):
        for c in self.cards:
            if cardStr==c.cardStr:
                card=c
                self.cards.remove(c)
                return card
        
class StardardDeck(Deck):
    def __init__(self):
        self.cards=[]
        suits = "cdhs"
        values= "23456789TJQKA"
        for name in values:
            for suit in suits:
                self.put(name+suit)
                
    def __repr__(self):
        return "Standard deck of cards:{0} remaining".format(len(self.cards))
    
class Player():
    def __init__(self):
        self.cards=[]
        
    def cardCount(self):
        return len(self.cards)
    
    #從牌組取幾張牌，預設抽出第一張牌
    def addCard(self, deck, cardStr=None):
        if cardStr==None:
            self.cards.append(deck.deal())
        else:
            for c in cardStr.split():
                self.cards.append(deck.draw(c))
    
    def strRepr(self):
        return ' '.join([card.cardStr for card in self.cards])
                
    
# 順子
def straight(rank):
    for i in range(len(rank)-4):
        R = rank[i:i+5]
        if max(R)-min(R)==4 and len(set(R))==5:
            return max(R)
    #順子A2345的情況
    if rank[0]==14 and rank[-4:]==[5,4,3,2]:
        return 5
    return False
    
#回傳數字陣列恰好出現n次的數字，降序排列
def n_kind(rank, n):
    return sorted([k for k,v in Counter(rank).items() if v==n], reverse=True)


"""
cards 的格式為字串如 "5d 5s 9c 9d 9h" 來表示一手牌
輸出為 [9,9,9,5,5] 降序排列
參數repeat表示是否去重複，
比如說repeat=False時，output[9,5]
"""
def card_rank(cards, repeat=True):
    f = lambda x: x if repeat else set(x)
    return sorted(f(map(lambda s: '0123456789TJQKA'.index(s[0]), cards.split())), reverse=True)

"""
cards 的格式為字串如 "5d 5s 9c 9d 9h" 來表示一手牌
回傳出現最多次的花色點數，降序排列，例如([9,5],'d')
"""
def card_rankForMostSuit(cards):
    suit=[s for r,s in cards.split()]
    most_suit= max(suit, key=lambda s: suit.count(s))
    rank=sorted(['0123456789TJQKA'.index(r) for r,s in cards.split() if s==most_suit], reverse=True)
    return rank, most_suit


"""
hand 的格式為字串如 "5d 5s 9c 9d 9h" 來表示一手牌
判斷手牌屬於何種牌型
"""
def hand_rank(hand):
    rank = card_rank(hand)
    rank_nonrepeat = card_rank(hand, repeat=False)
    ranks_suits=card_rankForMostSuit(hand)[0]
    
    flush = len(ranks_suits)>=5 and ranks_suits
    _straight = straight(rank_nonrepeat)
    straightFlush = flush and straight(ranks_suits)
    
    single, pair,three_kind, four_kind = (n_kind(rank, i) for i in range(1,5))
    
    if straightFlush:
        return (9,straightFlush)
    if four_kind:
        head = four_kind[0]
        return (8,four_kind[0], max(filter(lambda r:r!=head,rank)))
    if len(three_kind)>=2 or three_kind and pair:
        head = three_kind[0]
        return (7,head, max(filter(lambda r:r!=head,rank)))
    if flush:
        return (6, *flush[:5])
    if _straight:
        return (5,_straight)
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
    
    deck=StardardDeck()
    deck.shuffule()
    for i in deck.cards:
        i.showing=True
    Tom=Player()
    
    # 隨機抽7張牌測試牌型
    for i in range(7):
        Tom.addCard(deck)
    print(Tom.cards)
    print(card_rankForMostSuit(Tom.strRepr()))
    print(hand_rank(Tom.strRepr()))

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
    print(pokerSort(hands))
    for hand in hands:
        print(hand, hand_rank(hand))
