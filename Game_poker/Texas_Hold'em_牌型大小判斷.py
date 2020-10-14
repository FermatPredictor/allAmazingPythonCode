"""
程式功能:
可以在任意不重複的5~7張牌中找出最大的牌型，
並能夠判斷兩副牌的大小。
"""
import random
from collections import Counter
from itertools import groupby

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
    cards 的格式為字串如 "5d 5s 9c 9d 9h" 來表示一手牌
    輸出為 [9,9,9,5,5] 降序排列
    """
    return sorted(map(lambda s: '0123456789TJQKA'.index(s[0]), cards.split()), reverse=True)


def groupby_suit(cards):
    """
    cards 的格式為字串如 "5d 5s 9c 9d 9h" 來表示一手牌，
    group card by 花色，如{'c': [9], 'd': [9, 5], 'h': [9], 's': [5]}
    """
    cards = sorted(cards.split(), key=lambda x:x[1])
    return {k:sorted(map(lambda c: '0123456789TJQKA'.index(c[0]), group), reverse=True) \
             for k,group in groupby(cards, lambda x:x[1])}


def hand_rank(hand):
    """
    hand 的格式為字串如 "5d 5s 9c 9d 9h" 來表示一手牌
    判斷手牌屬於何種牌型
    """
    rank = card_rank(hand)
    suit_gp = groupby_suit(hand)
    
    flush = sorted(filter(lambda v: len(v)>=5, suit_gp.values()), reverse=True)
    _straight = straight(rank)
    straightFlush = sorted(filter(lambda v: len(v)>=5 and straight(v), suit_gp.values()), reverse=True)
    
    single, pair,three_kind, four_kind = (n_kind(rank, i) for i in range(1,5))
    
    if straightFlush:
        return (9,max(straightFlush[0], key = lambda x: 1 if x==14 else x))
    if four_kind:
        head = four_kind[0]
        return (8,four_kind[0], max(filter(lambda r:r!=head,rank)))
    if len(three_kind)>=2 or three_kind and pair:
        head = three_kind[0]
        return (7,head, max(filter(lambda r:r!=head,rank)))
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
    
    deck=StardardDeck()
    deck.shuffule()
    for card in deck.cards:
        card.showing=True
    Tom=Player()
    
    # 隨機抽7張牌測試牌型
    for i in range(7):
        Tom.addCard(deck)
    print(Tom.cards)
    print(groupby_suit(Tom.strRepr()))
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
